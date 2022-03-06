# How to do a release?

Here are the steps that need to be done when creating a release.

1. Move proposals into ADRs or FDRs.
2. Generate mkdocs.
3. Generate/Update the `CHANGELOG.md` document.
   * Use scripts to achieved this.
4. Add and sign an annotated tag release - `vX.X.X.` format.
5. Create a release in Github.
6. Check if the `README.md` needs to be updated.
7. Update configuration files (poetry).
8. Merge changes into `master`.
9. [Publish](https://python-poetry.org/docs/cli/#publish) a package to poetry.
