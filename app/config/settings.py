from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    env_file=".env",
    environments=True,
    load_dotenv=True,
    env_switcher="SYMBIUS_ENV",
    settings_file_encoding='utf-8',
    env_nested_delimiter="."
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
