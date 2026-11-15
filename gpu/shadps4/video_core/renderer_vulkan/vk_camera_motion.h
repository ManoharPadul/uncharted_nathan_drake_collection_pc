// SPDX-License-Identifier: GPL-2.0-or-later
// bbport: camera motion vectors for temporal upscaling (docs/upscaler.md). The scene constants
// give the camera of each frame; the previous one is kept here. BB_DEBUG_MOTION=1 blends the
// motion vectors as colors into the frame before it is copied to the display.

#pragma once

#include <array>
#include <vector>

#include "common/types.h"
#include "video_core/renderer_vulkan/vk_common.h"
#include "video_core/buffer_cache/buffer.h"
#include "video_core/texture_cache/image.h"

namespace VideoCore {
class TextureCache;
}

namespace Vulkan {

class Instance;
class Scheduler;
class Runtime;
class ObjectMotion;

class CameraMotion {
public:
    CameraMotion(const Instance& instance, Scheduler& scheduler,
                 VideoCore::TextureCache& texture_cache, Runtime& runtime);
    ~CameraMotion();
    void InvalidateHistory() { current.valid = previous.valid = false; }
    void SetObjectMotion(ObjectMotion* motion) noexcept {
        object_motion = motion;
    }
    /// This frame's object motion image (after RecordMotion), for the debug view; or null.
    vk::ImageView ObjectMotionView() const noexcept;
    vk::Image ObjectMotionImage(u32 width, u32 height) const noexcept;

    void SetJitter(std::array<float, 2> value) noexcept {
        previous_jitter = jitter;
        jitter = value;
    }

    [[nodiscard]] bool Enabled() const noexcept {
        return debug_overlay || for_upscaler;
    }

    /// Both cameras and the scene depth of the current frame are known; in VelocityMode the
    /// velocity pass's camera and the scene depth.
    [[nodiscard]] bool Ready() const noexcept {
        return velocity_mode ? velocity_camera.valid && depth_id
                             : current.valid && previous.valid && depth_id;
    }
    /// bbport: BB_VELOCITY_PS=<pixel shader hash,...> (Uncharted): the game's camera velocity
    /// pass (for its motion blur). Its constants give this frame's view from depth and the
    /// previous frame's projection (OnVelocityConstants); no scene constants are needed then.
    /// Its first target holds distortion (heat haze, shockwaves), the second the camera motion
    /// scaled by the motion blur setting, zero with the default ("Object"): neither is read.
    [[nodiscard]] bool VelocityMode() const noexcept {
        return velocity_mode;
    }
    [[nodiscard]] bool IsVelocityShader(u64 ps_hash) const noexcept;
    /// The velocity pass's constant buffer (`dwords` of it).
    void OnVelocityConstants(const float* data, u32 dwords);
    /// Records the motion vector pass from the velocity pass's camera into `motion_view`
    /// (RG16F storage, General), pixels, previous minus current; zero without that camera.
    void RecordVelocity(vk::CommandBuffer cmdbuf, vk::ImageView depth_view,
                        vk::ImageView motion_view, u32 width, u32 height);
    [[nodiscard]] VideoCore::ImageId Depth() const noexcept {
        return depth_id;
    }
    /// The render size in the scene constants (the game's viewport; its targets may be
    /// allocated larger, e.g. 1916x1080 for a 1916x1078 scene), or zero before the first camera.
    [[nodiscard]] std::array<u32, 2> RenderSize() const noexcept {
        return render_size;
    }
    /// Vertical field of view and near/far planes of the current camera.
    [[nodiscard]] float VerticalFov() const noexcept;
    [[nodiscard]] float Near() const noexcept;
    // Current projection, previous projection, and row Z of previous-view * inverse-view.
    [[nodiscard]] std::array<std::array<float, 4>, 3> TaaDepthParameters() const noexcept;

    /// Records the motion vector pass: `depth_view` (depth aspect, General layout) into
    /// `motion_view` (RG16F storage, General), pixels, previous minus current.
    void RecordMotion(vk::CommandBuffer cmdbuf, vk::ImageView depth_view, vk::ImageView motion_view,
                      u32 width, u32 height);

    /// A bound constant buffer of 864 bytes: checks the scene constant signature.
    void OnConstants(const float* data);

    /// The G-buffer pass (5+ color targets): its depth is the scene depth.
    void OnGBufferPass(VideoCore::ImageId depth);

    /// The pass copying the finished frame (`frame`, the last target drawn) to the display: the
    /// frame's depth and camera are complete. Records the debug overlay, starts a new frame.
    void OnDisplayPass(VideoCore::ImageId frame);

private:
    struct Camera {
        std::array<float, 12> view{};     ///< world to view, 3x4 rows
        std::array<float, 12> inv_view{}; ///< view to world, 3x4 rows
        std::array<float, 4> proj{};      ///< x scale, y scale, z scale, z offset
        bool valid = false;
    };

    void Overlay(VideoCore::ImageId frame);

    const Instance& instance;
    Scheduler& scheduler;
    VideoCore::TextureCache& texture_cache;
    Runtime& runtime;
    bool debug_overlay = false;
    bool for_upscaler = false;
    vk::UniqueDescriptorSetLayout motion_desc_layout;
    vk::UniquePipelineLayout motion_pipeline_layout;
    vk::UniquePipeline motion_pipeline;

    ObjectMotion* object_motion = nullptr;
    Camera current, previous;
    bool frame_has_camera = false;
    std::array<float, 2> jitter{}, previous_jitter{};
    std::array<u32, 2> render_size{};
    VideoCore::ImageId depth_id{};
    bool velocity_mode = false;
    std::vector<u64> velocity_shaders;
    /// The velocity pass's camera this frame: view position from depth and uv, and the 3x4
    /// view to previous clip (x, y, w rows).
    struct VelocityCamera {
        std::array<float, 12> to_previous_clip{};
        std::array<float, 4> uv_to_view{}; ///< view x = z (a u + c), view y = z (b v + d)
        std::array<float, 2> depth_to_z{}; ///< z = y / (depth - x)
        bool valid = false;
    } velocity_camera;

    vk::UniqueDescriptorSetLayout desc_layout;
    vk::UniquePipelineLayout pipeline_layout;
    vk::UniquePipeline overlay_pipeline;
    /// Debug: the last two finished frames (RGBA8 packed), for the reprojection check.
    std::unique_ptr<VideoCore::Buffer> frames[2];
    u32 frame_index = 0;
};

} // namespace Vulkan
