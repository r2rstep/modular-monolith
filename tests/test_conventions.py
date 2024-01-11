from pathlib import Path
import subprocess
import sysconfig

from importlinter.cli import lint_imports
import pytest
import toml


def test_ruff():
    ruff = Path(sysconfig.get_path("scripts")) / "ruff"

    # below print ensures PyCharm is able to link to the failing files
    print("\n")  # noqa: T201
    stdout, stderr, exit_code = _run([ruff, "check", "."])
    assert exit_code == 0, f"ruff check failed: {stdout}"
    stdout, stderr, exit_code = _run([ruff, "format", "--check", "."])
    assert exit_code == 0, f"ruff format check failed: {stdout}"


def _run(cmd: list[str]) -> tuple[str, str, int]:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # wait for the process to terminate
    out, err = process.communicate()
    errcode = process.returncode

    return out.decode("utf-8"), err.decode("utf-8"), errcode


@pytest.fixture(scope="session")
def existing_modules():
    modules = list(Path(__file__).parent.parent.glob("modules/**/core"))
    modules = [str(module)[str(module).find("/modules/") :] for module in modules]
    return [module.lstrip("/").rstrip("/core").replace("/", ".") for module in modules]


@pytest.fixture(scope="session")
def import_linter_contracts(pyproject_toml_path):
    with pyproject_toml_path.open("r") as f:
        pyproject_toml = toml.load(f)

    return pyproject_toml["tool"]["importlinter"]["contracts"]


def test_all_modules_listed_in_modules_layers_import_linter_section(existing_modules, import_linter_contracts):
    modules_listed_in_contracts = next(
        contract for contract in import_linter_contracts if contract["name"] == "Modules layers"
    )["containers"]

    assert set(modules_listed_in_contracts) == set(existing_modules)


def test_all_modules_listed_in_modules_interfaces_import_linter_section(existing_modules, import_linter_contracts):
    modules_listed_in_contracts = next(
        contract for contract in import_linter_contracts if contract["name"] == "Modules interfaces"
    )["modules"]

    assert set(modules_listed_in_contracts) == set(existing_modules)


def test_import_linter(pyproject_toml_path):
    assert lint_imports(str(pyproject_toml_path)) == 0
