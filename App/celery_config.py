from os import environ
import ssl

task_serializer = "pickle"
result_serializer = "pickle"
event_serializer = "json"
accept_content = ["application/json", "application/x-python-serialize"]
result_accept_content = ["application/json", "application/x-python-serialize"]
timezone = "Europe/Oslo"
enable_utc = True

broker_url = f"amqps://llmgzyix:WZZdL_6mmwvoawt58_gYYJV4veF8dOZm@beaver.rmq.cloudamqp.com/llmgzyix"
result_backend = f"db+postgresql+psycopg2://postgres:PkkneZrSFsnJR6B@db.vfhoydxvxuesxhrcdnmx.supabase.co:5432/postgres"

# SSL/TLS and SNI configuration
# broker_use_ssl = {
#     "ssl_cert_reqs": ssl.CERT_NONE,
#     "ssl_match_hostname": False,
#     "ssl_check_hostname": False,
#     "ssl_sni": "master.cache--j5zxzwppzvjs.addon.code.run",
# }
