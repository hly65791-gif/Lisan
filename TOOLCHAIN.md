# Gradle Toolchain Contract

For Android projects, the skill must report all of these before claiming a build is verified:

- Java executable/version
- system Gradle executable/version, if present
- project Wrapper files and JAR checksum
- configured Gradle distribution URL
- AGP/Kotlin versions
- actual build command
- actual exit code
- verified APK/AAB path and SHA-256 when produced

A missing system Gradle executable is not an error if the project Wrapper is complete and runnable. A missing Wrapper JAR may be repaired with the bootstrapper when network access is available.
