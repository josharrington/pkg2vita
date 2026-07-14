FROM archlinux:base

# Disable interactive prompts and cache
RUN echo 'Verity = Off' >> /etc/pacman.conf && \
    pacman -Sy --noconfirm --needed pacman git base-devel 7zip python

# Create non-root user for makepkg (which refuses to run as root)
RUN useradd -m -U builduser && \
    chown builduser:builduser /home/builduser

# Build pkg2zip from AUR PKBUILD as non-root user (build only, no install)
USER builduser
WORKDIR /home/builduser
RUN git clone https://aur.archlinux.org/pkg2zip.git pkg2zip && \
    cd pkg2zip && \
    makepkg -s && \
    cd ..

# Switch back to root to install the built package
USER root
RUN pacman -U /home/builduser/pkg2zip/pkg2zip-*.pkg.tar.zst --noconfirm && \
    rm -rf /home/builduser/pkg2zip

COPY unpack.py /unpack.py

RUN rm -rf /var/cache/pacman/pkg /var/lib/pacman/sync

WORKDIR /zip

CMD ["python", "/unpack.py", "/zip"]
