from fastapi import (
    Depends,
    params,
)
from fastapi_limiter.depends import (
    RateLimiter,
)
from pyrate_limiter.abstracts.rate import (
    Duration,
    Rate,
)
from pyrate_limiter.limiter import (
    Limiter,
)


class RequestRateLimiter(RateLimiter):
    """Request rate limiter."""

    def __init__(
        self,
        seconds: int,
        limit: int,
    ) -> None:
        """
        Initialize the request rate limiter.

        Parameters
        ----------
        seconds : int
            number of seconds for requests

        limit : int
            limit on a number of requests per time
        """
        limiter = Limiter(Rate(limit, Duration.SECOND * seconds))
        super().__init__(limiter=limiter)


def dep_rate_limiter_getter(
    seconds: int,
    limit: int = 1,
) -> params.Depends:
    """
    Get dependency on rate limiter.

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
        dependency=RequestRateLimiter(
            seconds=seconds,
            limit=limit,
        ),
    )
