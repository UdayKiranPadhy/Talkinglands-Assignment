from app.config import Config
from app.repository.connection import ConnectionFactory
from app.repository.spatial_db.points import PointsRepository
from app.repository.spatial_db.polygon import PolygonRepository
from lagom import Container, Singleton
from lagom.integrations.fast_api import FastApiIntegration
from typing import TypeVar, Generic, Any, Type


T = TypeVar("T")


class TypedContainer(Container, Generic[T]):
    """A container with type hints for dependency resolution"""

    def __getitem__(self, dep_type: Type[T]) -> T:
        """Get a dependency with proper type hinting"""
        return super().__getitem__(dep_type)


class ContainerBuilder:
    @classmethod
    def get_container(cls) -> TypedContainer[Any]:
        container = TypedContainer[Any]()

        container[Config] = Singleton(lambda: Config())

        def _create_connection_factory(c: TypedContainer[Any]) -> ConnectionFactory:
            return ConnectionFactory(
                c[Config].db.host,
                c[Config].db.user,
                c[Config].db.password,
            )

        def _connect_points_repository(c: TypedContainer[Any]) -> PointsRepository:
            return PointsRepository(
                c[ConnectionFactory].connect("spatial_db", "spatial_data")
            )
        
        def _connect_polygon_repository(c: TypedContainer[Any]) -> PolygonRepository:
            return PolygonRepository(
                c[ConnectionFactory].connect("spatial_db", "spatial_data")
            )

        container[ConnectionFactory] = Singleton(_create_connection_factory)
        container[PointsRepository] = Singleton(_connect_points_repository)
        container[PolygonRepository] = Singleton(_connect_polygon_repository)

        return container


lagom_container = ContainerBuilder.get_container()

container = FastApiIntegration(lagom_container)
