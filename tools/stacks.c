/* Prints every thread of a process with two stack walks: dbghelp unwinding (host code with
 * unwind data) and the frame-pointer chain (guest code). Raw addresses plus the module list;
 * tools/stacks.py turns them into names. Build: clang -O2 tools/stacks.c -o out/stacks.exe -ldbghelp
 * Usage: stacks.exe PID */
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <dbghelp.h>
#include <tlhelp32.h>
#include <psapi.h>
#include <stdio.h>
#include <stdlib.h>

typedef HRESULT (WINAPI *GetDescription)(HANDLE, PWSTR *);

int main(int argc, char **argv) {
    if (argc < 2) { fputs("usage: stacks PID\n", stderr); return 1; }
    DWORD pid = (DWORD)strtoul(argv[1], NULL, 10);
    HANDLE process = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!process) { fprintf(stderr, "cannot open process %lu\n", pid); return 1; }
    SymSetOptions(SYMOPT_DEFERRED_LOADS);
    SymInitialize(process, NULL, TRUE);
    HMODULE modules[1024]; DWORD needed = 0;
    EnumProcessModules(process, modules, sizeof(modules), &needed);
    for (unsigned i = 0; i < needed / sizeof(HMODULE); ++i) {
        MODULEINFO info; char name[MAX_PATH];
        GetModuleInformation(process, modules[i], &info, sizeof(info));
        GetModuleBaseNameA(process, modules[i], name, sizeof(name));
        printf("module %llx %lx %s\n", (unsigned long long)info.lpBaseOfDll, info.SizeOfImage, name);
    }
    GetDescription describe = (GetDescription)GetProcAddress(GetModuleHandleA("kernel32.dll"), "GetThreadDescription");
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    THREADENTRY32 entry = {.dwSize = sizeof(entry)};
    for (BOOL ok = Thread32First(snapshot, &entry); ok; ok = Thread32Next(snapshot, &entry)) {
        if (entry.th32OwnerProcessID != pid) continue;
        HANDLE thread = OpenThread(THREAD_ALL_ACCESS, FALSE, entry.th32ThreadID);
        if (!thread) continue;
        PWSTR description = NULL;
        char name[128] = "";
        if (describe && SUCCEEDED(describe(thread, &description)) && description) {
            WideCharToMultiByte(CP_UTF8, 0, description, -1, name, sizeof(name), NULL, NULL);
            LocalFree(description);
        }
        SuspendThread(thread);
        CONTEXT context = {.ContextFlags = CONTEXT_FULL};
        if (GetThreadContext(thread, &context)) {
            printf("thread %lu \"%s\" rip=%llx rsp=%llx rbp=%llx\n", entry.th32ThreadID, name,
                   context.Rip, context.Rsp, context.Rbp);
            CONTEXT walk = context;
            STACKFRAME64 frame = {0};
            frame.AddrPC.Offset = walk.Rip; frame.AddrPC.Mode = AddrModeFlat;
            frame.AddrFrame.Offset = walk.Rbp; frame.AddrFrame.Mode = AddrModeFlat;
            frame.AddrStack.Offset = walk.Rsp; frame.AddrStack.Mode = AddrModeFlat;
            printf("  unwind");
            for (int depth = 0; depth < 32; ++depth) {
                if (!StackWalk64(IMAGE_FILE_MACHINE_AMD64, process, thread, &frame, &walk, NULL,
                                 SymFunctionTableAccess64, SymGetModuleBase64, NULL) || !frame.AddrPC.Offset) break;
                printf(" %llx", frame.AddrPC.Offset);
            }
            printf("\n  frames %llx", context.Rip);
            unsigned long long rbp = context.Rbp;
            for (int depth = 0; depth < 32 && rbp; ++depth) {
                unsigned long long pair[2]; SIZE_T got = 0;
                if (!ReadProcessMemory(process, (void *)rbp, pair, sizeof(pair), &got) || got != sizeof(pair) || pair[0] <= rbp) break;
                printf(" %llx", pair[1]);
                rbp = pair[0];
            }
            printf("\n");
        }
        ResumeThread(thread);
        CloseHandle(thread);
    }
    return 0;
}
