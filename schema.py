import pydantic


class CreateAds(pydantic.BaseModel):
    header: str
    description: str
    owner: str