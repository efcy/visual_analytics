import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class LogStatus(pydantic_v1.BaseModel):
    """
    Id assigned by django
    """
    id: typing.Optional[int] = None

    """
    Foreign key to the log the image belongs to
    """
    log_id: typing.Optional[int] = pydantic_v1.Field(default=None)
    
    """
    ball_model_frames
    """
    ball_model_frames: typing.Optional[int] = None

    """
    camera_matrix_frames
    """
    camera_matrix_frames: typing.Optional[int] = None

    """
    camera_matrix_top_frames
    """
    camera_matrix_top_frames: typing.Optional[int] = pydantic_v1.Field(default=None)
    
    """
    field_percept_frames
    """
    field_percept_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    field_percept_top_frames
    """
    field_percept_top_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    goal_percept_frames
    """
    goal_percept_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    goal_percept_top_frames
    """
    goal_percept_top_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    ransacLine_percept_frames
    """
    ransacLine_percept_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    ransac_circle_percept_2018_frames
    """
    ransac_circle_percept_2018_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    shortLine_percept_frames
    """
    shortLine_percept_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    scanLine_edgel_percept_frames
    """
    scanLine_edgel_percept_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    scanLine_edgel_percept_top_frames
    """
    scanLine_edgel_percept_top_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    odometry_data_frames
    """
    odometry_data_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_cognition_frames
    """
    num_cognition_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_motion_frames
    """
    num_motion_frames: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_jpg_bottom
    """
    num_jpg_bottom: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_jpg_top
    """
    num_jpg_top: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_bottom
    """
    num_bottom: typing.Optional[str] = pydantic_v1.Field(default=None)

    """
    num_top
    """
    num_top: typing.Optional[str] = pydantic_v1.Field(default=None)


    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}