#！usr/bin bash
export PROJECT_DIR=$PWD
export BUILD_DIR=$PROJECT_DIR/build

#输出目录
mkdir -p $BUILD_DIR

BUILD_DATE=`date +%Y%m%d`
CONFIGURATION='Release'
SCHEME_NAME='GreenTownLife'
WORKSPACE_NAME='GreenTownLife'

#蒲公英
#UKEY='c23784bcc4797236ecb6db5c012ef8c3'
#APIKEY='2fd28a7b0c3cd053d8fb1c4380472e8d'

#1.git
git reset --hard
git pull
echo "拉取代码成功"

#2.pod配置
pod install
echo '更新pod成功...'

#3.clean
xcodebuild clean -workspace $WORKSPACE_NAME.xcworkspace -configuration $CONFIGURATION -scheme $SCHEME_NAME || echo 'clean failed'

#4.archive
xcodebuild archive \
-workspace "$WORKSPACE_NAME.xcworkspace" \
-scheme "$SCHEME_NAME" \
-configuration "$CONFIGURATION" \
-archivePath "build/GreenTownLife.xcarchive" \
clean \
build \
-derivedDataPath "build/tmp" || echo "archive failed..."

#5.export
xcodebuild -exportArchive \
-archivePath "build/GreenTownLife.xcarchive" \
-exportPath "build/ipa/$BUILD_DATE" \
-exportOptionsPlist 'build/GreenTownLife.xcarchive/info.plist' || echo "export .ipa failed..."

#6.重命名ipa
cd ./build/ipa/$BUILD_DATE
mv GreenTownLife.ipa GreenTownLife_$BUILD_DATE.ipa

#修改plist
# sed '8 a<key>method</key><string>enterprise</string>' -i tmp/info.plist
# rm -rf $BUILD_DIR

#6.upload
echo "开始上传ipa文件到蒲公英平台..."
cd $PROJECT_DIR
python3 pgyer_upload.py

# rm -rf $BUILD_DIR
