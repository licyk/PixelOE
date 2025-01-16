from torchvision.transforms.functional import to_tensor
from PIL import Image

from pixeloe.torch.pixelize import pixelize_pytorch
from pixeloe.torch.outline import outline_expansion
from pixeloe.torch.utils import to_numpy, pre_resize
from pixeloe.torch.minmax import dilate_cont, erode_cont, KERNELS
from pixeloe.torch.env import TORCH_COMPILE


if __name__ == "__main__":
    from tqdm import trange

    img = Image.open("./img/snow-leopard.png")

    img_t = to_tensor(img).cuda().half()[None]
    oe_t, w = outline_expansion(img_t, 6, 6, 8, 10, 3)
    oe = Image.fromarray(to_numpy(oe_t)[0])
    oe.save("./img/snow-leopard-oe-orig.png")

    patch_size = 4
    target_size = 360
    thickness = 3

    img_t = (
        pre_resize(img, target_size=target_size, patch_size=patch_size).cuda().half()
    )

    dilate_t = dilate_cont(img_t, KERNELS[thickness], 1)
    dilate_img = Image.fromarray(to_numpy(dilate_t)[0])
    dilate_img.save("./img/snow-leopard-dilate.png")

    erode_t = erode_cont(img_t, KERNELS[thickness], 1)
    erode_img = Image.fromarray(to_numpy(erode_t)[0])
    erode_img.save("./img/snow-leopard-erode.png")

    oe_t, w = outline_expansion(img_t, thickness, thickness, patch_size, 10, 3)
    oe = Image.fromarray(to_numpy(oe_t)[0])
    oe.save("./img/snow-leopard-oe.png")
    w = Image.fromarray(w[0, 0].float().cpu().numpy().clip(0, 1) * 255).convert("L")
    w.save("./img/snow-leopard-w.png")

    pixel_art_t = pixelize_pytorch(
        img_t,
        target_size=target_size,
        patch_size=patch_size,
        thickness=thickness,
        do_color_match=True,
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel.png")

    pixel_art_t = pixelize_pytorch(
        img_t,
        target_size=target_size,
        patch_size=patch_size,
        thickness=thickness,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-256c.png")

    pixel_art_t = pixelize_pytorch(
        img_t,
        target_size=target_size,
        patch_size=patch_size,
        thickness=thickness,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="ordered",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-256c-d.png")

    pixel_art_t = pixelize_pytorch(
        img_t,
        target_size=target_size,
        patch_size=patch_size,
        thickness=thickness,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="error_diffusion",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-256c-ed.png")

    pixel_art_t = pixelize_pytorch(
        pre_resize(img, target_size=320, patch_size=4).cuda(),
        target_size=320,
        patch_size=4,
        thickness=3,
        do_color_match=True,
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-lg.png")

    pixel_art_t = pixelize_pytorch(
        pre_resize(img, target_size=320, patch_size=4).cuda(),
        target_size=320,
        patch_size=4,
        thickness=3,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-lg-256c.png")

    pixel_art_t = pixelize_pytorch(
        pre_resize(img, target_size=320, patch_size=4).cuda(),
        target_size=320,
        patch_size=4,
        thickness=3,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="ordered",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-lg-256c-d.png")

    pixel_art_t = pixelize_pytorch(
        pre_resize(img, target_size=320, patch_size=4).cuda(),
        target_size=320,
        patch_size=4,
        thickness=3,
        do_color_match=True,
        do_quant=True,
        K=256,
        quant_mode="error_diffusion",
    )
    pixel_art = Image.fromarray(to_numpy(pixel_art_t)[0])
    pixel_art.save("./img/snow-leopard-pixel-lg-256c-ed.png")

    print("Start speed test:")
    print(f"  {target_size=}")
    print(f"  {patch_size=}")
    print(f"  {thickness=}")
    print(f"  {TORCH_COMPILE=}")
    # Warmup
    pixelize_pytorch(
        img_t.repeat(8, 1, 1, 1),
        target_size=target_size,
        patch_size=patch_size,
        thickness=thickness,
        do_color_match=False,
        do_quant=False,
    )
    for _ in trange(500, smoothing=0.01):
        pixel_art_t = pixelize_pytorch(
            img_t.repeat(8, 1, 1, 1),
            target_size=target_size,
            patch_size=patch_size,
            thickness=thickness,
            do_color_match=False,
            do_quant=False,
        )
    print("Speed test done")
