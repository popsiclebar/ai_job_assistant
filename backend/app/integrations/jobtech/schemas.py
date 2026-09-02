"""Models the subset of JobTech's search response consumed by this application.
Unknown provider fields are ignored so harmless upstream additions do not break searches."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class JobTechModel(BaseModel):
    """Apply tolerant parsing consistently to external JobTech payloads."""

    model_config = ConfigDict(extra="ignore")


class JobTechTotal(JobTechModel):
    """Hold the number of matching advertisements reported by JobTech."""

    value: int = 0


class JobTechTaxonomyItem(JobTechModel):
    """Represent one JobTech taxonomy value when only its display label is needed."""

    label: str | None = None


class JobTechDescription(JobTechModel):
    """Hold the plain-text job description used by later fit evaluation."""

    text: str = ""


class JobTechEmployer(JobTechModel):
    """Hold the employer identity exposed in a JobTech advertisement."""

    name: str | None = None


class JobTechApplicationDetails(JobTechModel):
    """Hold the external URL used to submit an application."""

    url: str | None = None


class JobTechWorkplaceAddress(JobTechModel):
    """Hold source geography fields used to build a readable normalized location."""

    city: str | None = None
    municipality: str | None = None
    region: str | None = None
    country: str | None = None


class JobTechHit(JobTechModel):
    """Model one current job advertisement returned by JobTech search."""

    id: str
    headline: str
    relevance: float | None = None
    webpage_url: str | None = None
    application_deadline: datetime | None = None
    number_of_vacancies: int | None = None
    description: JobTechDescription = Field(default_factory=JobTechDescription)
    employment_type: JobTechTaxonomyItem | None = None
    working_hours_type: JobTechTaxonomyItem | None = None
    duration: JobTechTaxonomyItem | None = None
    employer: JobTechEmployer | None = None
    application_details: JobTechApplicationDetails | None = None
    experience_required: bool | None = None
    occupation: JobTechTaxonomyItem | None = None
    workplace_model: JobTechTaxonomyItem | None = None
    workplace_address: JobTechWorkplaceAddress | None = None
    publication_date: datetime | None = None


class JobTechSearchResult(JobTechModel):
    """Model JobTech search metadata and the returned advertisement page."""

    total: JobTechTotal = Field(default_factory=JobTechTotal)
    positions: int = 0
    query_time_in_millis: int | None = None
    result_time_in_millis: int | None = None
    hits: list[JobTechHit] = Field(default_factory=list)
