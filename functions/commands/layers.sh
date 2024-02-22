python3.11 -m pip install --target=. -r ../requirements.txt 


rm -rf *.dist-info
find . -name "tests" -type d | xargs -I{} rm -rf {}
find . -name "docs" -type d | xargs -I{} rm -rf {}
find . -name "__pycache__" -type d | xargs -I{} rm -rf {}
rm -rf boto*

  aws lambda publish-layer-version --layer-name  my-layername  --zip-file fileb://my-layername.zip --compatible-runtimes "python3.10" "python3.11" "python3.12"