#!/usr/bin/env python3
import os
import json

out = os.popen('oc get clusterdeployment -A -ojson').read()
cd_json_items = json.loads(out)["items"]

for item in cd_json_items:
    labels = item["metadata"]["labels"]
    if not labels.get("hive.openshift.io/version-major-minor"):
        print("No hive version label on cluster, exiting")
        continue

    if labels.get("hive.openshift.io/version-major-minor") and int(labels["hive.openshift.io/version-major-minor"].split(".")[1]) < 13:
        print("Version less than v4.13, exiting")
        continue

    if labels.get("ext-managed.openshift.io/legacy-ingress-support"):
        print("ext-managed.openshift.io/legacy-ingress-support label already exists, moving to next cluster")
        continue
    else:
        print("ext-managed.openshift.io/legacy-ingress-support label does not exist and cluster is v4.13 or greater. Labelling as legacy-ingress: false.")
        namespace = item["metadata"]["namespace"]
        name = item["metadata"]["name"]
        cmd = f'oc annotate --dry-run clusterdeployment -n {namespace} {name} ext-managed.openshift.io/legacy-ingress-support="false"'
        print(f"Running {cmd}")

        out = os.popen(cmd)
        print(out.read())