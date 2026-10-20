# Research Delta - Mobile and cross-platform delivery

Review date: 2026-10-19
Owner: mobile-platform
Outcome: recommendation changed
Confidence: high

## Source changes

- Reviewed Expo SDK 58: <https://expo.dev/changelog/sdk-58>.
- Reviewed React Native release history: <https://reactnative.dev/blog/>.
- Reviewed Flutter 3.47 documentation changes: <https://docs.flutter.dev/release/whats-new>.

## Decision

Expo/RN upgrades must remain SDK-paired and migration-tested; SDK 58 / RN 0.88 and iOS 27 lifecycle changes are operationally material. Flutter remains a valid cross-platform alternative, with 3.47 adding stable widget previews and expanded SwiftPM/Kotlin migration guidance. Do not auto-upgrade mobile baselines from version discovery alone.

## Follow-up

- Validate store availability and native-module compatibility for each selected project before adoption.
