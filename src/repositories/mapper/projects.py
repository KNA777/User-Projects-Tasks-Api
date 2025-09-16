from src.models import ProjectsOrm
from src.repositories.mapper.base import DataMapper
from src.schemas.projects import Projects


class ProjectMapper(DataMapper):

    db_model = ProjectsOrm
    schema = Projects
