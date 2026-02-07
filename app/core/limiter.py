from typing import override

from fastapi import Depends, params
from fastapi_limiter.depends import RateLimiter
from pyrate_limiter import Duration, Limiter, Rate


class _FastAPIRateLimiter(RateLimiter):
    @override
    def __init__(
        self,
        seconds: int,
        limit: int,
    ) -> None:
        limiter = Limiter(Rate(limit, Duration.SECOND * seconds))
        super().__init__(limiter=limiter)


def dep_rate_limiter_getter(
    seconds: int,
    limit: int = 1,
) -> params.Depends:
    """Get dependencies on rate limiter.

    Parameters
    ----------
    seconds : int
        time interval in seconds

    limit : int, optional
        number of requests allowed within interval, by default 1

    Returns
    -------
    params.Depends
        dependency on limiter
    """
    return Depends(
        _FastAPIRateLimiter(
            seconds=seconds,
            limit=limit,
        )
    )
