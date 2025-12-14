# セットアップ方法 / Setup Instructions

## uv を使った環境構築 / Environment Setup with uv

このプロジェクトでは `uv` を使って Python 依存関係を管理し、再現性を確保しています。

This project uses `uv` to manage Python dependencies and ensure reproducibility.

### 必要要件 / Requirements

- Python 3.8 - 3.11 (Python 3.12+ は wrf-python と互換性がありません / Python 3.12+ is not compatible with wrf-python)
- uv パッケージマネージャー / uv package manager

### uv のインストール / Installing uv

```bash
# pip を使ってインストール / Install via pip
pip install uv
```

### 依存関係のインストール / Installing Dependencies

```bash
# プロジェクトディレクトリで / In the project directory
uv sync
```

これにより `uv.lock` ファイルに基づいて、すべての依存関係が正確なバージョンでインストールされます。

This will install all dependencies with exact versions based on the `uv.lock` file.

### スクリプトの実行 / Running Scripts

```bash
# uv を使ってスクリプトを実行 / Run scripts with uv
uv run python wrf_trajectory.py
uv run python mkpts.py
```

### 依存関係のテスト / Testing Dependencies

netCDF4 ライブラリが正しく動作することを確認するテスト:

Test to verify netCDF4 library works correctly:

```bash
# 開発用依存関係をインストール / Install dev dependencies
uv sync --extra dev

# pytest でテストを実行 / Run tests with pytest
uv run pytest test_netcdf4.py -v

# または直接実行も可能 / Or run directly (legacy)
uv run python test_netcdf4.py
```

## 注意事項 / Notes

### wrf-python について / About wrf-python

`wrf-python` はビルド時に `numpy.distutils` (numpy 2.0 で削除) に依存しており、Python 3.12+ との互換性問題があります。そのため、`pyproject.toml` には含まれていません。

`wrf-python` has build-time dependencies on `numpy.distutils` (removed in numpy 2.0) and compilation requirements that are incompatible with Python 3.12+. Therefore, it is not included in `pyproject.toml`.

Python 3.11 以下の環境で wrf-python が必要な場合は、別途インストールしてください:

If you need wrf-python in a Python 3.11 or earlier environment, install it separately:

```bash
# システム依存関係をインストール / Install system dependencies
sudo apt-get update
sudo apt-get install -y gfortran gcc g++ libnetcdf-dev libnetcdff-dev libhdf5-dev pkg-config

# Python 3.11 以下の環境で / In Python 3.11 or earlier environment
# ビルドに必要な依存関係をインストール (2段階で実行)
# Install build dependencies (in two steps)
# ステップ1: numpy を先にインストール (Cython が numpy に依存)
# Step 1: Install numpy first (Cython depends on numpy)
uv pip install "numpy<2.0" "setuptools<70" "wheel"
# ステップ2: Cython と他の依存関係
# Step 2: Cython and other dependencies
uv pip install "Cython<3.0" "wrapt"

# 環境変数を設定 / Set environment variables
export NETCDF=$(nc-config --prefix)
export HDF5=$(nc-config --prefix)
export HDF5_DIR=/usr
export NETCDF4_DIR=$(nc-config --prefix)
export USE_NCCONFIG=1

# wrf-python をインストール / Install wrf-python
uv pip install --no-build-isolation wrf-python
```

### geocat-f2py について / About geocat-f2py

`geocat-f2py` はコンパイル済みのバイナリとして配布されていますが、Fortran 拡張モジュールが含まれていない場合があります。GitHub Actions CI では、ソースから再ビルドして Fortran モジュールを確実にコンパイルします。

`geocat-f2py` is distributed as a pre-compiled binary, but may not include Fortran extension modules. In GitHub Actions CI, it is rebuilt from source to ensure Fortran modules are compiled.

システム依存関係のインストールと再ビルド方法:

System dependencies installation and rebuild instructions:

```bash
# Fortran コンパイラと netCDF ライブラリをインストール
# Install Fortran compiler and netCDF libraries
sudo apt-get update
sudo apt-get install -y gfortran gcc g++ libnetcdf-dev libnetcdff-dev libhdf5-dev pkg-config

# ビルドツールと numpy<2.0 をインストール（重要）
# Install build tools and numpy<2.0 (important)
uv pip install "numpy<2.0" "setuptools<70" "wheel"
uv pip install "Cython<3.0"

# geocat-f2py をソースから再ビルド（--no-build-isolation で既存の numpy を使用）
# Rebuild geocat-f2py from source (use --no-build-isolation to use existing numpy)
uv pip install --force-reinstall --no-binary geocat-f2py --no-build-isolation geocat-f2py

# インストール確認 / Verify installation
uv run python -c "import geocat.f2py; from geocat.f2py import rcm2rgrid; print('Success')"
```

**注意**: ソースからのビルドには時間がかかりますが、Fortran 拡張モジュールが確実に利用できるようになります。

**Note**: Building from source takes time but ensures Fortran extension modules are available.

## 従来の方法 / Traditional Method

uv を使わない場合は、以下の手動インストールも可能です:

If not using uv, you can also manually install dependencies:

```bash
pip install numpy netCDF4 wrf-python geocat-f2py pandas matplotlib
```

ただし、この方法では依存関係のバージョンが `uv.lock` と異なる可能性があります。

However, this method may result in different dependency versions than `uv.lock`.
