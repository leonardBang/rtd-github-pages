#!/bin/bash
set -x

# step-1: install dependencies
apt-get update
apt-get -y install git rsync python3-pip python3-git python3-stemmer python3-virtualenv python3-setuptools
python3 -m pip install -U sphinx==4.1.1 myst-parser pygments sphinx-rtd-theme

export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
export REPO_NAME="${GITHUB_REPOSITORY##*/}"
temp_docs_root=`mktemp -d`

# step-2: build sites for all branches(for multiple versioned docs), excludes 'HEAD' and 'gh-pages'
make -C docs clean
branches="`git for-each-ref '--format=%(refname:lstrip=-1)' refs/remotes/origin/ | grep -viE '^(HEAD|gh-pages)$'`"
for current_branch in ${branches}; do
   export current_branch
   git checkout ${current_branch}

   # skip the branch that has no docs
   if [ ! -e 'docs/conf.py' ]; then
      echo -e "\tINFO: Couldn't find 'docs/conf.py' for branch: ${current_branch}, just skip this branch"
      continue
   fi
   echo "INFO: Building sites for branch: ${current_branch}"
   sphinx-build -b html docs/ docs/_build/html/${current_branch}

   # copy the build content to temp dir
   rsync -av "docs/_build/html/" "${temp_docs_root}/"
 
done
 
git checkout master
git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

# step-3: push build sites to  gh-pages branch
pushd "${temp_docs_root}"
git init
git remote add deploy "https://token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
git checkout -b gh-pages

touch .nojekyll
cat > index.html <<EOF
<!DOCTYPE html>
<html>
   <head>
      <title>helloWorld Docs</title>
      <meta http-equiv = "refresh" content="0; url='/${REPO_NAME}/master/'" />
   </head>
   <body>
      <p>Please wait while you're redirected to our <a href="/${REPO_NAME}/master/">documentation</a>.</p>
   </body>
</html>
EOF

git add .
git commit -m "Generated docs from commit ${GITHUB_SHA}"
git push deploy gh-pages --force
 
popd

exit 0