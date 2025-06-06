"""
System specific functions.

MicroPython module: https://docs.micropython.org/en/v1.24.0/library/sys.html

CPython module: :mod:`python:sys` https://docs.python.org/3/library/sys.html .
"""

from __future__ import annotations
import sys
from _typeshed import Incomplete, MaybeNone, OptExcInfo, ProfileFunction, TraceFunction, structseq
from _typeshed.importlib import MetaPathFinderProtocol, PathEntryFinderProtocol
from builtins import object as _object
from collections.abc import AsyncGenerator, Callable
from io import TextIOWrapper
from types import FrameType, ModuleType, TracebackType
from typing import Callable, overload, Any, Final, Literal, NoReturn, Protocol, TextIO, TypeVar, final
from typing_extensions import Awaitable, TypeVar, TypeAlias
from _mpy_shed import IOBase_mp, _mp_implementation

_T = TypeVar("_T")

# see https://github.com/python/typeshed/issues/8513#issue-1333671093 for the rationale behind this alias
_ExitCode: TypeAlias = str | int | None
_OptExcInfo: TypeAlias = OptExcInfo  # noqa: Y047  # TODO: obsolete, remove fall 2022 or later

# ----- sys variables -----
if sys.platform != "win32":
    abiflags: str
argv: list[str]
# base_exec_prefix: str
# base_prefix: str
byteorder: Literal["little", "big"]
# builtin_module_names: Sequence[str]  # actually a tuple of strings
# copyright: str
if sys.platform == "win32":
    dllhandle: int
# dont_write_bytecode: bool
# displayhook: Callable[[object], Any]
# excepthook: Callable[[type[BaseException], BaseException, TracebackType | None], Any]
# exec_prefix: str
# executable: str
# float_repr_style: Literal["short", "legacy"]
# hexversion: int
# last_type: type[BaseException] | None
# last_value: BaseException | None
# last_traceback: TracebackType | None
if sys.version_info >= (3, 12):
    last_exc: BaseException  # or undefined.
maxsize: int
# maxunicode: int
# meta_path: list[MetaPathFinderProtocol]
modules: dict[str, ModuleType]
if sys.version_info >= (3, 10):
    orig_argv: list[str]
path: list[str]
# path_hooks: list[Callable[[str], PathEntryFinderProtocol]]
# path_importer_cache: dict[str, PathEntryFinderProtocol | None]
platform: str
if sys.version_info >= (3, 9):
    platlibdir: str
# prefix: str
# pycache_prefix: str | None
ps1: object
ps2: object

# TextIO is used instead of more specific types for the standard streams,
# since they are often monkeypatched at runtime. At startup, the objects
# are initialized to instances of TextIOWrapper, but can also be None under
# some circumstances.
#
# To use methods from TextIOWrapper, use an isinstance check to ensure that
# the streams have not been overridden:
#
# if isinstance(sys.stdout, io.TextIOWrapper):
#    sys.stdout.reconfigure(...)
stdin: TextIO | MaybeNone
stdout: TextIO | MaybeNone
stderr: TextIO | MaybeNone

if sys.version_info >= (3, 10):
    stdlib_module_names: frozenset[str]

__stdin__: Final[TextIOWrapper | None]  # Contains the original value of stdin
__stdout__: Final[TextIOWrapper | None]  # Contains the original value of stdout
__stderr__: Final[TextIOWrapper | None]  # Contains the original value of stderr
tracebacklimit: int
version: str
# api_version: int
# warnoptions: Any
#  Each entry is a tuple of the form (action, message, category, module,
#    lineno)
if sys.platform == "win32":
    winver: str
_xoptions: dict[Any, Any]

# Type alias used as a mixin for structseq classes that cannot be instantiated at runtime
# This can't be represented in the type system, so we just use `structseq[Any]`
_UninstantiableStructseq: TypeAlias = structseq[Any]

# flags: _flags

if sys.version_info >= (3, 10):
    _FlagTuple: TypeAlias = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, bool, int, int]
else:
    _FlagTuple: TypeAlias = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, bool, int]

@final
class _flags(_UninstantiableStructseq, _FlagTuple):
    @property
    def debug(self) -> int: ...
    @property
    def inspect(self) -> int: ...
    @property
    def interactive(self) -> int: ...
    @property
    def optimize(self) -> int: ...
    @property
    def dont_write_bytecode(self) -> int: ...
    @property
    def no_user_site(self) -> int: ...
    @property
    def no_site(self) -> int: ...
    @property
    def ignore_environment(self) -> int: ...
    @property
    def verbose(self) -> int: ...
    @property
    def bytes_warning(self) -> int: ...
    @property
    def quiet(self) -> int: ...
    @property
    def hash_randomization(self) -> int: ...
    @property
    def isolated(self) -> int: ...
    @property
    def dev_mode(self) -> bool: ...
    @property
    def utf8_mode(self) -> int: ...
    if sys.version_info >= (3, 10):
        @property
        def warn_default_encoding(self) -> int: ...  # undocumented
    if sys.version_info >= (3, 11):
        @property
        def safe_path(self) -> bool: ...

# float_info: _float_info

@final
class _float_info(structseq[float], tuple[float, int, int, float, int, int, int, int, float, int, int]):
    @property
    def max(self) -> float: ...  # DBL_MAX
    @property
    def max_exp(self) -> int: ...  # DBL_MAX_EXP
    @property
    def max_10_exp(self) -> int: ...  # DBL_MAX_10_EXP
    @property
    def min(self) -> float: ...  # DBL_MIN
    @property
    def min_exp(self) -> int: ...  # DBL_MIN_EXP
    @property
    def min_10_exp(self) -> int: ...  # DBL_MIN_10_EXP
    @property
    def dig(self) -> int: ...  # DBL_DIG
    @property
    def mant_dig(self) -> int: ...  # DBL_MANT_DIG
    @property
    def epsilon(self) -> float: ...  # DBL_EPSILON
    @property
    def radix(self) -> int: ...  # FLT_RADIX
    @property
    def rounds(self) -> int: ...  # FLT_ROUNDS

# hash_info: _hash_info

@final
class _hash_info(structseq[Any | int], tuple[int, int, int, int, int, str, int, int, int]):
    @property
    def width(self) -> int: ...
    @property
    def modulus(self) -> int: ...
    @property
    def inf(self) -> int: ...
    @property
    def nan(self) -> int: ...
    @property
    def imag(self) -> int: ...
    @property
    def algorithm(self) -> str: ...
    @property
    def hash_bits(self) -> int: ...
    @property
    def seed_bits(self) -> int: ...
    @property
    def cutoff(self) -> int: ...  # undocumented

implementation: _mp_implementation

class _implementation:
    name: str
    version: _version_info
    hexversion: int
    cache_tag: str
    # Define __getattr__, as the documentation states:
    # > sys.implementation may contain additional attributes specific to the Python implementation.
    # > These non-standard attributes must start with an underscore, and are not described here.
    def __getattr__(self, name: str) -> Any: ...

# int_info: _int_info

@final
class _int_info(structseq[int], tuple[int, int, int, int]):
    @property
    def bits_per_digit(self) -> int: ...
    @property
    def sizeof_digit(self) -> int: ...
    @property
    def default_max_str_digits(self) -> int: ...
    @property
    def str_digits_check_threshold(self) -> int: ...

_ThreadInfoName: TypeAlias = Literal["nt", "pthread", "pthread-stubs", "solaris"]
_ThreadInfoLock: TypeAlias = Literal["semaphore", "mutex+cond"] | None

@final
class _thread_info(_UninstantiableStructseq, tuple[_ThreadInfoName, _ThreadInfoLock, str | None]):
    @property
    def name(self) -> _ThreadInfoName: ...
    @property
    def lock(self) -> _ThreadInfoLock: ...
    @property
    def version(self) -> str | None: ...

# thread_info: _thread_info
_ReleaseLevel: TypeAlias = Literal["alpha", "beta", "candidate", "final"]

@final
class _version_info(_UninstantiableStructseq, tuple[int, int, int, _ReleaseLevel, int]):
    @property
    def major(self) -> int: ...
    @property
    def minor(self) -> int: ...
    @property
    def micro(self) -> int: ...
    @property
    def releaselevel(self) -> _ReleaseLevel: ...
    @property
    def serial(self) -> int: ...

version_info: _version_info

def call_tracing(func: Callable[..., _T], args: Any, /) -> _T: ...
def _clear_type_cache() -> None: ...
def _current_frames() -> dict[int, FrameType]: ...
def _getframe(depth: int = 0, /) -> FrameType: ...
def _debugmallocstats() -> None: ...
def __displayhook__(object: object, /) -> None: ...
def __excepthook__(exctype: type[BaseException], value: BaseException, traceback: TracebackType | None, /) -> None: ...
def exc_info() -> OptExcInfo: ...

if sys.version_info >= (3, 11):
    def exception() -> BaseException | None: ...

@overload
def exit(retval: object = 0, /) -> NoReturn:
    """
    Terminate current program with a given exit code. Underlyingly, this
    function raise as `SystemExit` exception. If an argument is given, its
    value given as an argument to `SystemExit`.
    """
    ...

@overload
def exit(retval: object = 0, /) -> NoReturn:
    """
    Terminate current program with a given exit code. Underlyingly, this
    function raise as `SystemExit` exception. If an argument is given, its
    value given as an argument to `SystemExit`.
    """
    ...

def getallocatedblocks() -> int: ...
def getdefaultencoding() -> str: ...

if sys.platform != "win32":
    def getdlopenflags() -> int: ...

def getfilesystemencoding() -> str: ...
def getfilesystemencodeerrors() -> str: ...
def getrefcount(object: Any, /) -> int: ...
def getrecursionlimit() -> int: ...
def getsizeof(obj: object, default: int = ...) -> int: ...
def getswitchinterval() -> float: ...
def getprofile() -> ProfileFunction | None: ...
def setprofile(function: ProfileFunction | None, /) -> None: ...
def gettrace() -> TraceFunction | None: ...
@overload
def settrace(tracefunc) -> None:
    """
    Enable tracing of bytecode execution.  For details see the `CPython
    documentation `<https://docs.python.org/3/library/sys.html#sys.settrace>.

    This function requires a custom MicroPython build as it is typically not
    present in pre-built firmware (due to it affecting performance).  The relevant
    configuration option is *MICROPY_PY_SYS_SETTRACE*.
    """
    ...

@overload
def settrace(tracefunc) -> None:
    """
    Enable tracing of bytecode execution.  For details see the `CPython
    documentation `<https://docs.python.org/3/library/sys.html#sys.settrace>.

    This function requires a custom MicroPython build as it is typically not
    present in pre-built firmware (due to it affecting performance).  The relevant
    configuration option is *MICROPY_PY_SYS_SETTRACE*.
    """
    ...

if sys.platform == "win32":
    # A tuple of length 5, even though it has more than 5 attributes.
    @final
    class _WinVersion(_UninstantiableStructseq, tuple[int, int, int, int, str]):
        @property
        def major(self) -> int: ...
        @property
        def minor(self) -> int: ...
        @property
        def build(self) -> int: ...
        @property
        def platform(self) -> int: ...
        @property
        def service_pack(self) -> str: ...
        @property
        def service_pack_minor(self) -> int: ...
        @property
        def service_pack_major(self) -> int: ...
        @property
        def suite_mask(self) -> int: ...
        @property
        def product_type(self) -> int: ...
        @property
        def platform_version(self) -> tuple[int, int, int]: ...

    def getwindowsversion() -> _WinVersion: ...

def intern(string: str, /) -> str: ...
def is_finalizing() -> bool: ...
def breakpointhook(*args: Any, **kwargs: Any) -> Any: ...

__breakpointhook__ = breakpointhook  # Contains the original value of breakpointhook

if sys.platform != "win32":
    def setdlopenflags(flags: int, /) -> None: ...

def setrecursionlimit(limit: int, /) -> None: ...
def setswitchinterval(interval: float, /) -> None: ...
def gettotalrefcount() -> int: ...  # Debug builds only

if sys.version_info < (3, 9):
    def getcheckinterval() -> int: ...  # deprecated
    def setcheckinterval(n: int, /) -> None: ...  # deprecated

if sys.version_info < (3, 9):
    # An 11-tuple or None
    def callstats() -> tuple[int, int, int, int, int, int, int, int, int, int, int] | None: ...

# Doesn't exist at runtime, but exported in the stubs so pytest etc. can annotate their code more easily.
class UnraisableHookArgs(Protocol):
    exc_type: type[BaseException]
    exc_value: BaseException | None
    exc_traceback: TracebackType | None
    err_msg: str | None
    object: _object

# unraisablehook: Callable[[UnraisableHookArgs], Any]

def __unraisablehook__(unraisable: UnraisableHookArgs, /) -> Any: ...
def addaudithook(hook: Callable[[str, tuple[Any, ...]], Any]) -> None: ...
def audit(event: str, /, *args: Any) -> None: ...

_AsyncgenHook: TypeAlias = Callable[[AsyncGenerator[Any, Any]], None] | None

@final
class _asyncgen_hooks(structseq[_AsyncgenHook], tuple[_AsyncgenHook, _AsyncgenHook]):
    @property
    def firstiter(self) -> _AsyncgenHook: ...
    @property
    def finalizer(self) -> _AsyncgenHook: ...

def get_asyncgen_hooks() -> _asyncgen_hooks: ...
def set_asyncgen_hooks(firstiter: _AsyncgenHook = ..., finalizer: _AsyncgenHook = ...) -> None: ...

if sys.platform == "win32":
    def _enablelegacywindowsfsencoding() -> None: ...

def get_coroutine_origin_tracking_depth() -> int: ...
def set_coroutine_origin_tracking_depth(depth: int) -> None: ...

# The following two functions were added in 3.11.0, 3.10.7, 3.9.14, and 3.8.14,
# as part of the response to CVE-2020-10735
def set_int_max_str_digits(maxdigits: int) -> None: ...
def get_int_max_str_digits() -> int: ...

if sys.version_info >= (3, 12):
    if sys.version_info >= (3, 13):
        def getunicodeinternedsize(*, _only_immortal: bool = False) -> int: ...
    else:
        def getunicodeinternedsize() -> int: ...

    def deactivate_stack_trampoline() -> None: ...
    def is_stack_trampoline_active() -> bool: ...
    # It always exists, but raises on non-linux platforms:
    if sys.platform == "linux":
        def activate_stack_trampoline(backend: str, /) -> None: ...
    else:
        def activate_stack_trampoline(backend: str, /) -> NoReturn: ...

    from . import _monitoring

    monitoring = _monitoring

@overload
def __mpy_has_no_atexit(func: Callable[[], None] | None, /) -> Callable[[], None] | None:
    """
    Register *func* to be called upon termination.  *func* must be a callable
    that takes no arguments, or ``None`` to disable the call.  The ``atexit``
    function will return the previous value set by this function, which is
    initially ``None``.

    Admonition:Difference to CPython
       :class: attention

       This function is a MicroPython extension intended to provide similar
       functionality to the :mod:`atexit` module in CPython.
    """
    ...

@overload
def __mpy_has_no_atexit(func: Callable[[], None] | None, /) -> Callable[[], None] | None:
    """
    Register *func* to be called upon termination.  *func* must be a callable
    that takes no arguments, or ``None`` to disable the call.  The ``atexit``
    function will return the previous value set by this function, which is
    initially ``None``.

    Admonition:Difference to CPython
       :class: attention

       This function is a MicroPython extension intended to provide similar
       functionality to the :mod:`atexit` module in CPython.
    """
    ...

@overload
def print_exception(exc: Exception | BaseException, file: IOBase_mp = stdout, /) -> None:
    """
    Print exception with a traceback to a file-like object *file* (or
    `sys.stdout` by default).

    Admonition:Difference to CPython
       :class: attention

       This is simplified version of a function which appears in the
       ``traceback`` module in CPython. Unlike ``traceback.print_exception()``,
       this function takes just exception value instead of exception type,
       exception value, and traceback object; *file* argument should be
       positional; further arguments are not supported. CPython-compatible
       ``traceback`` module can be found in `micropython-lib`.
    """
    ...

@overload
def print_exception(exc: Exception | BaseException, file: IOBase_mp = stdout, /) -> None:
    """
    Print exception with a traceback to a file-like object *file* (or
    `sys.stdout` by default).

    Admonition:Difference to CPython
       :class: attention

       This is simplified version of a function which appears in the
       ``traceback`` module in CPython. Unlike ``traceback.print_exception()``,
       this function takes just exception value instead of exception type,
       exception value, and traceback object; *file* argument should be
       positional; further arguments are not supported. CPython-compatible
       ``traceback`` module can be found in `micropython-lib`.
    """
    ...
