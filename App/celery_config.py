from os import environ
import ssl

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Oslo"
enable_utc = True

broker_url = f"rediss://default:8a715dd4651c8739b157d0ee0bb2d924@master.cache--j5zxzwppzvjs.addon.code.run:6379?ssl_cert_reqs=none"
result_backend = f"db+postgresql+psycopg2://postgres:PkkneZrSFsnJR6B@db.vfhoydxvxuesxhrcdnmx.supabase.co:5432/postgres"

# SSL/TLS and SNI configuration
broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE,
    "ssl_match_hostname": False,
    "ssl_check_hostname": False,
    "ssl_sni": "master.cache--j5zxzwppzvjs.addon.code.run",
}
