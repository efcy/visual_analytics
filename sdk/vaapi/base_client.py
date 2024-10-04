import os
import typing
import httpx

from .core.api_error import ApiError
from .core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .annotations.client import AnnotationsClient, AsyncAnnotationsClient
from .events.client import EventsClient #, AsyncAnnotationsClient
from .game.client import GameClient #, AsyncAnnotationsClient
from .logs.client import LogClient #, AsyncAnnotationsClient
from .cognition_representation.client import CognitionRepresentationClient #, AsyncAnnotationsClient
from .motion_representation.client import MotionRepresentationClient #, AsyncAnnotationsClient
from .behavior_options.client import BehaviorOptionClient #, AsyncAnnotationsClient
from .behavior_options_state.client import BehaviorOptionStateClient #, AsyncAnnotationsClient
from .behavior_frame_option.client import BehaviorFrameOptionClient #, AsyncAnnotationsClient
from .image.client import ImageClient #, AsyncAnnotationsClient
from .xabsl_symbol.client import XabslSymbolClient, AsyncXabslSymbolClient

class VaapiBase:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : LabelStudioEnvironment
        The environment to use for requests from the client. from .environment import LabelStudioEnvironment



        Defaults to LabelStudioEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from label_studio_sdk.client import LabelStudio

    client = LabelStudio(
        api_key="YOUR_API_KEY",
    )
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
        self.xabsl_symbol = XabslSymbolClient(client_wrapper=self._client_wrapper)
        
        
        #self.users = UsersClient(client_wrapper=self._client_wrapper)
        #self.actions = ActionsClient(client_wrapper=self._client_wrapper)
        #self.views = ViewsClient(client_wrapper=self._client_wrapper)
        #self.files = FilesClient(client_wrapper=self._client_wrapper)
        #self.projects = ProjectsClient(client_wrapper=self._client_wrapper)
        #self.ml = MlClient(client_wrapper=self._client_wrapper)
        #self.predictions = PredictionsClient(client_wrapper=self._client_wrapper)
        #self.tasks = TasksClient(client_wrapper=self._client_wrapper)
        #self.import_storage = ImportStorageClient(client_wrapper=self._client_wrapper)
        #self.export_storage = ExportStorageClient(client_wrapper=self._client_wrapper)
        #self.webhooks = WebhooksClient(client_wrapper=self._client_wrapper)
        #self.prompts = PromptsClient(client_wrapper=self._client_wrapper)
        #self.model_providers = ModelProvidersClient(client_wrapper=self._client_wrapper)
        #self.comments = CommentsClient(client_wrapper=self._client_wrapper)
        #self.workspaces = WorkspacesClient(client_wrapper=self._client_wrapper)

class AsyncVaapiBase:
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : LabelStudioEnvironment
        The environment to use for requests from the client. from .environment import LabelStudioEnvironment



        Defaults to LabelStudioEnvironment.DEFAULT



    api_key : typing.Optional[str]
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from label_studio_sdk.client import AsyncLabelStudio

    client = AsyncLabelStudio(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        api_key: typing.Optional[str] = os.getenv("VAT_API_TOKEN"),
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        if api_key is None:
            raise ApiError(
                body="The client must be instantiated be either passing in api_key or setting LABEL_STUDIO_API_KEY"
            )
        self._client_wrapper = AsyncClientWrapper(
            base_url=base_url,
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.xabsl_symbol = AsyncXabslSymbolClient(client_wrapper=self._client_wrapper)
        #self.annotations = AsyncAnnotationsClient(client_wrapper=self._client_wrapper)
        #self.users = AsyncUsersClient(client_wrapper=self._client_wrapper)
        #self.actions = AsyncActionsClient(client_wrapper=self._client_wrapper)
        #self.views = AsyncViewsClient(client_wrapper=self._client_wrapper)
        #self.files = AsyncFilesClient(client_wrapper=self._client_wrapper)
        #self.projects = AsyncProjectsClient(client_wrapper=self._client_wrapper)
        #self.ml = AsyncMlClient(client_wrapper=self._client_wrapper)
        #self.predictions = AsyncPredictionsClient(client_wrapper=self._client_wrapper)
        #self.tasks = AsyncTasksClient(client_wrapper=self._client_wrapper)
        #self.import_storage = AsyncImportStorageClient(client_wrapper=self._client_wrapper)
        #self.export_storage = AsyncExportStorageClient(client_wrapper=self._client_wrapper)
        #self.webhooks = AsyncWebhooksClient(client_wrapper=self._client_wrapper)
        #self.prompts = AsyncPromptsClient(client_wrapper=self._client_wrapper)
        #self.model_providers = AsyncModelProvidersClient(client_wrapper=self._client_wrapper)
        #self.comments = AsyncCommentsClient(client_wrapper=self._client_wrapper)
        #self.workspaces = AsyncWorkspacesClient(client_wrapper=self._client_wrapper)

