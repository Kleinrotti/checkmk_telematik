# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.155.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] CheckMK version: 1.6.0-latest, 2.0.0-latest, 2.1.0-latest
ARG VARIANT="2.4.0-latest"

FROM checkmk/check-mk-cloud:${VARIANT}
RUN /docker-entrypoint.sh /bin/true

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends nodejs gcc

ADD requirements.txt /tmp/requirements.txt
RUN PATH="/omd/sites/cmk/bin:${PATH}" \
    OMD_ROOT="/omd/sites/cmk" \
    /omd/sites/cmk/bin/pip3 install -r /tmp/requirements.txt

ENTRYPOINT ["/bin/bash"]