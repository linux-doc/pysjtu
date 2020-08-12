import re
from datetime import date, datetime
from async_property import async_property

from pysjtu import consts
from pysjtu.client.api import CourseLibMixin, ExamMixin, GPAMixin, ScheduleMixin, ScoreMixin, SelectionMixin
from pysjtu.client.base import BaseClient
from pysjtu.session import BaseSession, AsyncSession


class Client(SelectionMixin, ScheduleMixin, CourseLibMixin, ExamMixin, GPAMixin, ScoreMixin, BaseClient):
    """
    A pysjtu client with schedule query, score query, exam query, etc.

    Usage::

        >>> import pysjtu
        >>> s = pysjtu.AsyncSession(username="user@sjtu.edu.cn", password="something_secret")
        >>> client = pysjtu.Client(session=s)
        >>> sched = client.schedule(2019, 0)
        >>> sched
        [<ScheduleCourse 军事理论 week=[range(9, 17)] day=1 time=range(1, 3)>, ...]
        >>> sched.filter(time=range(3,5), day=range(2, 4))
        [<ScheduleCourse 程序设计思想与方法（C++） week=[range(1, 10), range(11, 17)] day=2 time=range(3, 5)>,
        <ScheduleCourse 大学英语（4） week=[range(1, 17)] day=3 time=range(3, 5)>]

    :param session: The :class:`Session` to be built upon.
    """
    _session: BaseSession
    _term_start: date

    def __init__(self, session: BaseSession):
        super().__init__()
        if not isinstance(session, BaseSession):
            raise TypeError("'session' isn't an instance of BaseSession.")
        self._session = session

        # noinspection PyTypeChecker
        self._term_start = None  # type: ignore

    @async_property
    async def term_start_date(self) -> date:
        """ Get the term start date for the current term. """
        if not self._term_start:
            raw = await self._session.get(consts.CALENDAR_URL + str(self.student_id))
            self._term_start = datetime.strptime(min(re.findall(r"\d{4}-\d{2}-\d{2}", await raw.text())), "%Y-%m-%d").date()
        return self._term_start

    # noinspection PyProtectedMember
    @async_property
    async def student_id(self) -> int:
        """ Get the student id of the current session. """
        if "student_id" not in self._session._cache_store:
            rtn = await self._session.get(consts.HOME_URL)
            self._session._cache_store["student_id"] = int(
                re.findall(r"(?<=id=\"sessionUserKey\" value=\")\d*", await rtn.text())[0])
        return self._session._cache_store["student_id"]


def create_client(username: str, password: str, _mocker_app=None) -> Client:
    """
    Create a new :class:`Client` with default options.
    To change :class:`AsyncSession` settings or preserve your session, use :class:`AsyncSession` and :class:`Client` instead.

    :param username: JAccount username.
    :param password: JAccount password.
    :param _mocker_app: An WSGI application to send requests to (for debug or test purposes).
    :return: an authenticated :class:`Client`.
    """
    sess = AsyncSession(username=username, password=password, _mocker_app=_mocker_app)
    return Client(session=sess)
