FROM ubuntu:18.04

WORKDIR /src

RUN apt update -q && apt install -y autoconf build-essential libssl-dev zlib1g-dev

COPY ./ /src
RUN  autoreconf \
	&& ./configure \
	&& make \
	&& make install


FROM ubuntu:18.04

RUN apt update -q && apt install -y libssl1.1 python3 python3-requests \
	&&  useradd -m -d /var/run/sshd -s /usr/sbin/nologin sshd  \
	&& mkdir /var/empty

COPY --from=0 /usr/local /usr/local
COPY entrypoint.py /entrypoint
COPY sync-authorized-keys.py /sync-authorized-keys
COPY rtunnel-shell /rtunnel-shell
ENTRYPOINT ["/entrypoint"]
