import os
import typing
import httpx

from .core.api_error import ApiError
from .core.client_wrapper import SyncClientWrapper
from .annotations.client import AnnotationsClient
from .events.client import EventsClient
from .game.client import GameClient
from .logs.client import LogClient
from .cognition_representation.client import CognitionRepresentationClient
from .motion_representation.client import MotionRepresentationClient
from .behavior_options.client import BehaviorOptionClient
from .behavior_options_state.client import BehaviorOptionStateClient
from .behavior_frame_option.client import BehaviorFrameOptionClient
from .image.client import ImageClient
from .xabsl_symbol_complete.client import XabslSymbolClientComplete
from .xabsl_symbol_sparse.client import XabslSymbolClientSparse
from .log_status.client import LogStatusClient
from .frame_filter.client import FrameFilterClient


class VaapiBase:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    ```python
    from label_studio_sdk.client import LabelStudio

    client = LabelStudio(
        api_key="YOUR_API_KEY",
    )
    ```
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        api_key: typing.Optional[str] = os.getenv("VAT_API_TOKEN"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting LABEL_STUDIO_API_KEY"
            )
        self._client_wrapper = SyncClientWrapper(
            base_url=base_url,
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.annotations = AnnotationsClient(client_wrapper=self._client_wrapper)
        self.events = EventsClient(client_wrapper=self._client_wrapper)
        self.games = GameClient(client_wrapper=self._client_wrapper)  
        self.logs = LogClient(client_wrapper=self._client_wrapper)
        self.cognition_repr = CognitionRepresentationClient(client_wrapper=self._client_wrapper)
        self.motion_repr = MotionRepresentationClient(client_wrapper=self._client_wrapper)
        self.behavior_option = BehaviorOptionClient(client_wrapper=self._client_wrapper)
        self.behavior_option_state = BehaviorOptionStateClient(client_wrapper=self._client_wrapper)
        self.behavior_frame_option = BehaviorFrameOptionClient(client_wrapper=self._client_wrapper)
        self.image = ImageClient(client_wrapper=self._client_wrapper)
        self.xabsl_symbol_complete = XabslSymbolClientComplete(client_wrapper=self._client_wrapper)
        self.xabsl_symbol_sparse = XabslSymbolClientSparse(client_wrapper=self._client_wrapper)
        self.log_status = LogStatusClient(client_wrapper=self._client_wrapper)
        self.frame_filter = FrameFilterClient(client_wrapper=self._client_wrapper)

