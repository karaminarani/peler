import functools
from typing import Callable, Union

from hydrogram import Client
from hydrogram.types import CallbackQuery, Message

from bot.helpers import helper_handlers


def authorized_users_only(
    func: Callable[[Client, Union[Message, CallbackQuery]], None]
) -> Callable[[Client, Union[Message, CallbackQuery]], None]:
    """
    Decorator to restrict access to authorized users only.

    This decorator ensures that only authorized users (admin users) can access the decorated function.
    If a user is not authorized, the behavior varies depending on the type of event:
    - For `CallbackQuery` events, it will send an alert message indicating "Not Yours!".

    Args:
        func (Callable[[Client, Union[Message, CallbackQuery]], None]):
            The function to be decorated. It should accept a `Client` and an event of type `Message` or `CallbackQuery`.

    Returns:
        Callable[[Client, Union[Message, CallbackQuery]], None]:
            The decorated function that performs an authorization check before executing the original function.
    """

    @functools.wraps(func)
    async def wrapper(client: Client, event: Union[Message, CallbackQuery]) -> None:
        # Check if the user is in the list of authorized admins
        if event.from_user.id not in helper_handlers.admins:
            if isinstance(event, CallbackQuery):
                await event.answer("Not Yours!", show_alert=True)

            return

        # Call the original function if the user is authorized
        await func(client, event)

    return wrapper
