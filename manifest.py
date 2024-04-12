import requests, zipfile, os, json

def create_manifest():
    path = 'html/firmware'

    files = os.listdir(path)

    for f in files:
        if f.endswith(".bin"):
            pos = f.find('full')-1
            if pos >= 0:
                base = f[0:pos]
                print(base)

                pos = f.find('MB_')+3
                ext = f.find('.bin')-1
                manifest = "{}{}{}.json".format(path, os.path.sep, f[0:pos-1])
                long_version = f[pos:ext]
                short_version = long_version.split('-')[0]
                if pos >= 0:
                    print(manifest)

                data = {"name":"openHASP", "version": short_version, "home_assistant_domain": "openhasp", "funding_url": "https://ko-fi.com/openhasp", "new_install_prompt_erase": True, "builds": "d"}
                builds = []
                if "gs-t3e" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "panlee" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "esp32-s3-" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "elecrow-s3-" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "seeed" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "sunton-4827" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "sunton-8048" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "esp32-terminal" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "ttgo-t7-s3" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                elif "wt-86-32-3zw1" in base:
                    builds.append({ "chipFamily": "ESP32-S2", "improv": False })
                elif "wt32-sc01-plus" in base:
                    builds.append({ "chipFamily": "ESP32-S3", "improv": False })
                else:
                    builds.append({ "chipFamily": "ESP32", "improv": False })
                parts = []
                parts.append({ "path": f, "offset": 0 })
                builds[0]["parts"] = parts
                data["builds"] = builds
                json_data = json.dumps(data, indent=4, sort_keys=False)
                print(json_data)
                with open(manifest, "w") as outfile:
                    outfile.write(json_data)

create_manifest()
