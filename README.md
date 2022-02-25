# artifactory-trash-restore

[![Build](https://github.com/tomtom-internal/artifactory-trash-restore/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/tomtom-internal/artifactory-trash-restore/actions/workflows/build.yml)

Tool to restore artifacts from Artifactory trashcan.

In situations where lot of artifacts in many directories got moved to the trashcan, Artifactory is not capable of restoring them in one go. The user gets from the UI or the REST API the following error:

```text
Failed to execute moveout items list to move
```

The only way to solve this is to restore the lowest folder with only artifacts inside. Doing this manually would result in lot of work. This is what this script is intended to do for you.

## Requirements

* Generate Artifactory access token
* Python 3.9

## Usage

```bash
python3 -mvenv env
source env/bin/activate
pip3 install -r requirements.txt

python3 artifactory-trash-restore.py --url https://artifactory.acme.org/artifactory --token "$ARTIFACTORY_ACCESS_TOKEN" my-repository/path/
```

## Contribution

[Pre-commit](https://pre-commit.com/) is used to validate your commits before submitting them to code review

* Make sure pre-commit is installed, e.g.,

    ```sh
    python3 -m pip install pre-commit
    ```

* Install pre-commit hook types

    ```sh
    pre-commit install --install-hooks -t pre-commit -t commit-msg
    ```

## License

Apache 2.0

## Author Information

See [CODEOWNERS](.github/CODEOWNERS).

---

Made with :green_heart:.
