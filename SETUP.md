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
# Python 3.11 以下の環境で / In Python 3.11 or earlier environment
uv pip install wrf-python
```

### geocat-f2py について / About geocat-f2py

`geocat-f2py` はコンパイルが必要なため、一部の環境ではインポートエラーが発生する可能性があります。システムに適切な Fortran コンパイラがインストールされていることを確認してください。

`geocat-f2py` requires compilation and may fail to import in some environments. Ensure you have proper Fortran compilers installed on your system.

## 従来の方法 / Traditional Method

uv を使わない場合は、以下の手動インストールも可能です:

If not using uv, you can also manually install dependencies:

```bash
pip install numpy netCDF4 wrf-python geocat-f2py pandas matplotlib
```

ただし、この方法では依存関係のバージョンが `uv.lock` と異なる可能性があります。

However, this method may result in different dependency versions than `uv.lock`.
