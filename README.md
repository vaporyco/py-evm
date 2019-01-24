# Python Implementation of the VVM

[![Join the chat at https://gitter.im/vaporyco/py-vvm](https://badges.gitter.im/vaporyco/py-vvm.svg)](https://gitter.im/vaporyco/py-vvm)
[![Documentation Status](https://readthedocs.org/projects/py-vvm/badge/?version=latest)](http://py-vvm.readthedocs.io/en/latest/?badge=latest)

[Documentation hosted by ReadTheDocs](http://py-vvm.readthedocs.io/en/latest/)


## Introducing Py-VVM

Py-VVM is a new implementation of the Vapory Virtual Machine written in
python. It is currently in active development but is quickly progressing
through the test suite provided by ethereum/tests. I have Vitalik, and the
existing PyEthereum code to thank for the quick progress I’ve made as many
design decisions were inspired, or even directly ported from the PyEthereum
codebase.

Py-VVM aims to eventually become the defacto python implementation of the VVM,
enabling a wide array of use cases for both public and private chains.
Development will focus on creating an VVM with a well defined API, friendly and
easy to digest documentation which can be run as a fully functional mainnet
node.

### Step 1: Alpha Release

The plan is to begin with an MVP, alpha-level release that is suitable for
testing purposes. We’ll be looking for early adopters to provide feedback on
our architecture and API choices as well as general feedback and bug finding.

#### Blog posts:

- https://medium.com/@pipermerriam/py-evm-part-1-origins-25d9ad390b


## Development
Py-VVM depends on a submodule of the common tests across all clients,
so you need to clone the repo with the `--recursive` flag. Example:

```sh
git clone --recursive git@github.com:vaporyco/py-vvm.git
```

Then install the required python packages via:

```sh
pip install -e . -r requirements-dev.txt
```


### Running the tests

You can run the tests with:

```sh
py.test tests
```

Or you can install `tox` to run the full test suite.


### Releasing

Pandoc is required for transforming the markdown README to the proper format to
render correctly on pypi.

For Debian-like systems:

```
apt install pandoc
```

Or on OSX:

```sh
brew install pandoc
```

To release a new version:

```sh
bumpversion $$VERSION_PART_TO_BUMP$$
git push && git push --tags
make release
```


#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, use bumpversion and specify which part to bump,
like `bumpversion minor` or `bumpversion devnum`.

If you are in a beta version, `bumpversion stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `bumpversion --new-version 4.0.0-alpha.1 devnum`
