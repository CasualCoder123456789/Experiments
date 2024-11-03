import os
import random
import sys
from typing import Sequence, Mapping, Any, Union
import torch


def get_value_at_index(obj: Union[Sequence, Mapping], index: int) -> Any:
    """Returns the value at the given index of a sequence or mapping.

    If the object is a sequence (like list or string), returns the value at the given index.
    If the object is a mapping (like a dictionary), returns the value at the index-th key.

    Some return a dictionary, in these cases, we look for the "results" key

    Args:
        obj (Union[Sequence, Mapping]): The object to retrieve the value from.
        index (int): The index of the value to retrieve.

    Returns:
        Any: The value at the given index.

    Raises:
        IndexError: If the index is out of bounds for the object and the object is not a mapping.
    """
    try:
        return obj[index]
    except KeyError:
        return obj["result"][index]


def find_path(name: str, path: str = None) -> str:
    """
    Recursively looks at parent folders starting from the given path until it finds the given name.
    Returns the path as a Path object if found, or None otherwise.
    """
    # If no path is given, use the current working directory
    if path is None:
        path = os.getcwd()

    # Check if the current directory contains the name
    if name in os.listdir(path):
        path_name = os.path.join(path, name)
        print(f"{name} found: {path_name}")
        return path_name

    # Get the parent directory
    parent_directory = os.path.dirname(path)

    # If the parent directory is the same as the current directory, we've reached the root and stop the search
    if parent_directory == path:
        return None

    # Recursively call the function with the parent directory
    return find_path(name, parent_directory)


def add_comfyui_directory_to_sys_path() -> None:
    """
    Add 'ComfyUI' to the sys.path
    """
    comfyui_path = find_path("ComfyUI")
    if comfyui_path is not None and os.path.isdir(comfyui_path):
        sys.path.append(comfyui_path)
        print(f"'{comfyui_path}' added to sys.path")


def add_extra_model_paths() -> None:
    """
    Parse the optional extra_model_paths.yaml file and add the parsed paths to the sys.path.
    """
    try:
        from main import load_extra_path_config
    except ImportError:
        print(
            "Could not import load_extra_path_config from main.py. Looking in utils.extra_config instead."
        )
        from utils.extra_config import load_extra_path_config

    extra_model_paths = find_path("extra_model_paths.yaml")

    if extra_model_paths is not None:
        load_extra_path_config(extra_model_paths)
    else:
        print("Could not find the extra_model_paths config file.")


add_comfyui_directory_to_sys_path()
add_extra_model_paths()


def import_custom_nodes() -> None:
    """Find all custom nodes in the custom_nodes folder and add those node objects to NODE_CLASS_MAPPINGS

    This function sets up a new asyncio event loop, initializes the PromptServer,
    creates a PromptQueue, and initializes the custom nodes.
    """
    import asyncio
    import execution
    from nodes import init_extra_nodes
    import server

    # Creating a new event loop and setting it as the default loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Creating an instance of PromptServer with the loop
    server_instance = server.PromptServer(loop)
    execution.PromptQueue(server_instance)

    # Initializing custom nodes
    init_extra_nodes()


from nodes import NODE_CLASS_MAPPINGS


def main():
    import_custom_nodes()
    with torch.inference_mode():
        unetloadergguf = NODE_CLASS_MAPPINGS["UnetLoaderGGUF"]()
        unetloadergguf_10 = unetloadergguf.load_unet(unet_name="flux1-dev-Q8_0.gguf")

        vaeloader = NODE_CLASS_MAPPINGS["VAELoader"]()
        vaeloader_11 = vaeloader.load_vae(vae_name="ae.safetensors")

        dualcliploadergguf = NODE_CLASS_MAPPINGS["DualCLIPLoaderGGUF"]()
        dualcliploadergguf_19 = dualcliploadergguf.load_clip(
            clip_name1="clip_l.safetensors",
            clip_name2="t5xxl_fp8_e4m3fn.safetensors",
            type="flux",
        )

        cliptextencodeflux = NODE_CLASS_MAPPINGS["CLIPTextEncodeFlux"]()
        cliptextencodeflux_15 = cliptextencodeflux.encode(
            clip_l="A dragon rising out of a volcano.Illustration_style",
            t5xxl="A dragon rising out of a volcano.",
            guidance=3.5,
            clip=get_value_at_index(dualcliploadergguf_19, 0),
        )

        loadimage = NODE_CLASS_MAPPINGS["LoadImage"]()
        loadimage_21 = loadimage.load_image(image="ComfyUI_00020_.png")

        vaeencode = NODE_CLASS_MAPPINGS["VAEEncode"]()
        vaeencode_23 = vaeencode.encode(
            pixels=get_value_at_index(loadimage_21, 0),
            vae=get_value_at_index(vaeloader_11, 0),
        )

        conditioningzeroout = NODE_CLASS_MAPPINGS["ConditioningZeroOut"]()
        ksampler = NODE_CLASS_MAPPINGS["KSampler"]()
        vaedecode = NODE_CLASS_MAPPINGS["VAEDecode"]()

        for q in range(1):
            conditioningzeroout_16 = conditioningzeroout.zero_out(
                conditioning=get_value_at_index(cliptextencodeflux_15, 0)
            )

            ksampler_3 = ksampler.sample(
                seed=random.randint(1, 2**64),
                steps=30,
                cfg=1,
                sampler_name="euler",
                scheduler="simple",
                denoise=0.8,
                model=get_value_at_index(unetloadergguf_10, 0),
                positive=get_value_at_index(cliptextencodeflux_15, 0),
                negative=get_value_at_index(conditioningzeroout_16, 0),
                latent_image=get_value_at_index(vaeencode_23, 0),
            )

            vaedecode_8 = vaedecode.decode(
                samples=get_value_at_index(ksampler_3, 0),
                vae=get_value_at_index(vaeloader_11, 0),
            )

            vaedecode_24 = vaedecode.decode(
                samples=get_value_at_index(vaeencode_23, 0),
                vae=get_value_at_index(vaeloader_11, 0),
            )


if __name__ == "__main__":
    main()
