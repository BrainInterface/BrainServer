import os
from typing import Any, Optional, Union

import torch
from tensorflow import keras

# pylint: disable=unsubscriptable-object
from brain_server.models import db
from brain_server.models.agent import Agent


def load_model(path: str, model_type: Optional[str] = None,
               ModelClass: Optional[Any] = None) -> Union[torch.nn.Module, keras.Model]:
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
    if model_type == 'keras':
        return keras.models.load_model(path)
    raise ValueError(f'model_type must be "pytorch" or "keras", but was {model_type}')


def save_model(path: str,
               model: Union[torch.nn.Module, keras.Model],
               model_type: Optional[str] = None) -> None:
    """
    Saves the model.
    :param path: Path to the save location.
    :param model: The model to save.
    :param model_type: Optional parameter of the model type. Must 'pytorch' or 'keras'. If model
    type is given. The method will try to guess it by file extension.
    """
    if model_type is None:
        model_type = _guess_model_type(path)
    if model_type == 'pytorch':
        torch.save(model.state_dict(), path)
    elif model_type == 'keras':
        model.save(path)
    else:
        raise ValueError(f'model_type must be "pytorch" or "keras", but was {model_type}')
    model_dto = Agent(model_type=model_type, path=path)
    db.session.add(model_dto)
    db.session.commit()


def _guess_model_type(path):
    _, extension = os.path.splitext(path)
    if extension in ('.pt', '.pth'):
        return 'pytorch'
    if extension in ('.h5', '.keras', '.pb'):
        return 'keras'
    raise IOError(f'Could not guess the model type from path: {path}')
