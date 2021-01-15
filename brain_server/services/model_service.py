import os
import torch
from typing import Any, Optional


def load_model(path: str, model_type: Optional[str], ModelClass: Optional[Any]) -> Any:
    """
    Loads a tensorflow or pytorch model.
    :param path: Path to model.
    :param model_type: Optional parameter of the model type. Must 'pytorch' or 'keras'. If model
    type is given. The method will try to guess it by file extension.
    :param ModelClass: Is required for pytorch. Is must be sub class of 'torch.nn.Module'
    :return: The loaded model.
    """
    if model_type is None:
        model_type = _guess_model_type(path)
    if model_type == 'pytorch':
        model: torch.nn.Module = ModelClass()
        checkpoint = torch.load(path)
        model.load_state_dict(checkpoint)
        return model
    elif model_type == 'keras':
        raise ImportError('Currently tensorflow is not supported for python 3.9.')
    else:
        raise ValueError(f'model_type must be "pytorch" or "keras", but was {model_type}')


def save_model(path: str) -> None:
    """
    Saves the model.
    :param path: Path to the save location.
    """


def _guess_model_type(path):
    _, extension = os.path.splitext(path)
    if extension == ('.pt' or '.pth'):
        return 'pytorch'
    elif extension == ('.h5' or '.keras'):
        return 'keras'
    else:
        raise IOError(f'Could not guess the model type.')
