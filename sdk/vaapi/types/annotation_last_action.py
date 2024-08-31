import typing

AnnotationLastAction = typing.Union[
    typing.Literal[
        "prediction",
        "propagated_annotation",
        "imported",
        "submitted",
        "updated",
        "skipped",
        "accepted",
        "rejected",
        "fixed_and_accepted",
        "deleted_review",
    ],
    typing.Any,
]