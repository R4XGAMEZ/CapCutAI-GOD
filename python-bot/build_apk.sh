#!/bin/bash
GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${GREEN}⚡ CapCut AI GOD - APK Builder by R4X${NC}"
echo ""
read -p "GitHub Username: " GITHUB_USER
read -p "GitHub Token: " GITHUB_TOKEN
read -p "Repo name [CapCutAI-GOD]: " input_repo
GITHUB_REPO="${input_repo:-CapCutAI-GOD}"

API="https://api.github.com"
AUTH="Authorization: token $GITHUB_TOKEN"
WORK_DIR="$HOME/CapCutAI"

pkg install -y curl git jq unzip 2>/dev/null

echo -e "\n${CYAN}[1/5] Checking repo...${NC}"
REPO_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -H "$AUTH" "$API/repos/$GITHUB_USER/$GITHUB_REPO")
if [ "$REPO_CHECK" != "200" ]; then
    echo "Creating repo..."
    curl -s -X POST "$API/user/repos" -H "$AUTH" -H "Content-Type: application/json" \
        -d "{\"name\":\"$GITHUB_REPO\",\"private\":false,\"auto_init\":true}" > /dev/null
    sleep 3
    echo "Repo created!"
else
    echo "Repo found!"
fi

upload_file() {
    local file_path="$1"
    local repo_path="$2"
    local content=$(base64 -w 0 "$file_path" 2>/dev/null || base64 "$file_path")
    SHA=$(curl -s -H "$AUTH" "$API/repos/$GITHUB_USER/$GITHUB_REPO/contents/$repo_path" | jq -r '.sha // empty')
    if [ -n "$SHA" ]; then
        curl -s -X PUT "$API/repos/$GITHUB_USER/$GITHUB_REPO/contents/$repo_path" \
            -H "$AUTH" -H "Content-Type: application/json" \
            -d "{\"message\":\"update\",\"content\":\"$content\",\"sha\":\"$SHA\"}" > /dev/null
    else
        curl -s -X PUT "$API/repos/$GITHUB_USER/$GITHUB_REPO/contents/$repo_path" \
            -H "$AUTH" -H "Content-Type: application/json" \
            -d "{\"message\":\"add\",\"content\":\"$content\"}" > /dev/null
    fi
    echo "  ✅ $repo_path"
}

echo -e "\n${CYAN}[2/5] Uploading files...${NC}"
find "$WORK_DIR" -type f | while read filepath; do
    rel_path="${filepath#$WORK_DIR/}"
    case "$rel_path" in
        .git/*|*/build/*|*.class|*.apk|"{"*) continue ;;
    esac
    upload_file "$filepath" "$rel_path"
done

echo -e "\n${CYAN}[3/5] Adding Gradle wrapper JAR...${NC}"
TEMP_JAR="$HOME/gradle-wrapper.jar"
curl -sL "https://github.com/gradle/gradle/raw/v8.4.0/gradle/wrapper/gradle-wrapper.jar" -o "$TEMP_JAR"
if [ -s "$TEMP_JAR" ]; then
    upload_file "$TEMP_JAR" "android-app/gradle/wrapper/gradle-wrapper.jar"
    rm "$TEMP_JAR"
fi

echo -e "\n${CYAN}[4/5] Triggering build...${NC}"
curl -s -X POST "$API/repos/$GITHUB_USER/$GITHUB_REPO/actions/workflows/build.yml/dispatches" \
    -H "$AUTH" -H "Content-Type: application/json" -d '{"ref":"main"}' > /dev/null
echo "Build triggered! Waiting (~5 min)..."
echo "Watch: https://github.com/$GITHUB_USER/$GITHUB_REPO/actions"

MAX_WAIT=600; ELAPSED=0; RUN_ID=""
while [ $ELAPSED -lt $MAX_WAIT ]; do
    sleep 20; ELAPSED=$((ELAPSED+20))
    RUN=$(curl -s -H "$AUTH" "$API/repos/$GITHUB_USER/$GITHUB_REPO/actions/runs?per_page=1")
    STATUS=$(echo "$RUN" | jq -r '.workflow_runs[0].status')
    CONCLUSION=$(echo "$RUN" | jq -r '.workflow_runs[0].conclusion')
    RUN_ID=$(echo "$RUN" | jq -r '.workflow_runs[0].id')
    echo -ne "\r  ⏳ $STATUS | ${ELAPSED}s elapsed..."
    if [ "$STATUS" = "completed" ]; then
        echo ""
        [ "$CONCLUSION" = "success" ] && echo "✅ Build SUCCESS!" && break
        echo "❌ Build FAILED! Check GitHub Actions." && exit 1
    fi
done

echo -e "\n${CYAN}[5/5] Downloading APK...${NC}"
ARTIFACT_ID=$(curl -s -H "$AUTH" "$API/repos/$GITHUB_USER/$GITHUB_REPO/actions/runs/$RUN_ID/artifacts" | jq -r '.artifacts[0].id')
APK_ZIP="$HOME/apk_dl.zip"
curl -sL -H "$AUTH" "$API/repos/$GITHUB_USER/$GITHUB_REPO/actions/artifacts/$ARTIFACT_ID/zip" -o "$APK_ZIP"
mkdir -p "$HOME/apk_out"
unzip -o "$APK_ZIP" -d "$HOME/apk_out/" > /dev/null 2>&1
APK=$(find "$HOME/apk_out" -name "*.apk" | head -1)
cp "$APK" "/sdcard/Download/CapCutAI-GOD.apk"
rm -rf "$HOME/apk_out" "$APK_ZIP"

echo ""
echo -e "${GREEN}╔══════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ APK READY!           ║${NC}"
echo -e "${GREEN}╚══════════════════════════╝${NC}"
echo "📱 /sdcard/Download/CapCutAI-GOD.apk"
echo "Files app se install karo!"
