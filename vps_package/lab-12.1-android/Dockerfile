# --- Stage 1: Build APK ---
FROM eclipse-temurin:17-jdk-jammy AS builder

ENV ANDROID_SDK_ROOT /opt/android-sdk
ENV PATH ${PATH}:${ANDROID_SDK_ROOT}/cmdline-tools/latest/bin:${ANDROID_SDK_ROOT}/platform-tools

RUN apt-get update && apt-get install -y wget unzip \
    && mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools \
    && wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O /tmp/cmdline-tools.zip \
    && unzip /tmp/cmdline-tools.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools \
    && mv ${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/latest \
    && rm /tmp/cmdline-tools.zip

RUN yes | sdkmanager --licenses \
    && sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0"

WORKDIR /app
COPY . .

# Generate gradle wrapper if missing (requires local gradle or we just install it)
# Generate gradle wrapper
RUN wget -q https://services.gradle.org/distributions/gradle-8.6-bin.zip -O /tmp/gradle.zip \
    && unzip -q /tmp/gradle.zip -d /opt \
    && rm /tmp/gradle.zip \
    && /opt/gradle-8.6/bin/gradle wrapper \
    && chmod +x gradlew \
    && ./gradlew assembleDebug --no-daemon --stacktrace

# --- Stage 2: Serve APK ---
FROM python:3.9-slim

WORKDIR /app
COPY --from=builder /app/app/build/outputs/apk/debug/app-debug.apk .

EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080"]
