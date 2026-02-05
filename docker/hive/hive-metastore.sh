#!/bin/bash
set -euo pipefail

JAR_DIR=/opt/aux-jars
HIVE_LIB_DIR=/opt/hive/lib
mkdir -p "$JAR_DIR"

if [ ! -f "$JAR_DIR/hadoop-aws-3.3.6.jar" ]; then
  curl -L -o "$JAR_DIR/hadoop-aws-3.3.6.jar" \
    https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.6/hadoop-aws-3.3.6.jar
fi

if [ ! -f "$JAR_DIR/aws-java-sdk-bundle-1.12.262.jar" ]; then
  curl -L -o "$JAR_DIR/aws-java-sdk-bundle-1.12.262.jar" \
    https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar
fi

export HIVE_AUX_JARS_PATH="$JAR_DIR"
export HADOOP_CLASSPATH="$JAR_DIR/*"

# Initialize metastore schema if needed (derby default)
if ! /opt/hive/bin/schematool -dbType derby -info >/dev/null 2>&1; then
  /opt/hive/bin/schematool -dbType derby -initSchema
fi

exec /opt/hive/bin/hive --service metastore
