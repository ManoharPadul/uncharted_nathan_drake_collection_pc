// SPDX-FileCopyrightText: Copyright 2025 shadPS4 Emulator Project
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

#include <atomic>

#include "common/bit_array.h"
#include "common/types.h"

namespace VideoCore {

constexpr u64 TRACKER_PAGE_BITS = 12; // 4K pages
constexpr u64 TRACKER_BYTES_PER_PAGE = 1ULL << TRACKER_PAGE_BITS;

constexpr u64 TRACKER_HIGHER_PAGE_BITS = 22; // each region is 4MB
constexpr u64 TRACKER_HIGHER_PAGE_SIZE = 1ULL << TRACKER_HIGHER_PAGE_BITS;
constexpr u64 TRACKER_HIGHER_PAGE_MASK = TRACKER_HIGHER_PAGE_SIZE - 1ULL;
constexpr u64 NUM_PAGES_PER_REGION = TRACKER_HIGHER_PAGE_SIZE / TRACKER_BYTES_PER_PAGE;

enum class Type {
    CPU,
    GPU,
};

using RegionBits = Common::BitArray<NUM_PAGES_PER_REGION>;

/// bbport: guest flips so far (Rasterizer::OnGuestFlip); the age of GPU data in pages.
inline std::atomic<u32> g_guest_frames{0};

/// bbport: a scheduler tick the GPU reaches only after the work being recorded now (a GPU write
/// marked now completes by then; BufferCache sets it).
inline u64 (*g_gpu_write_done_tick)() = nullptr;

} // namespace VideoCore
