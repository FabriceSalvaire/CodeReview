rm -rf repo-two-branches
mkdir repo-two-branches
cd repo-two-branches
git init

echo "foo" >> file1.txt
git add file1.txt
git commit -a -m "master/commit 1"

echo "baz" >> file1.txt
git commit -a -m "master/commit 2"

git checkout -b branche1
echo "foo" >> file2.txt
git add file2.txt
git commit -a -m "branche1/commit 1"

git checkout -b branche2
echo "foo" >> file3.txt
git add file3.txt
git commit -a -m "branche2/commit 1"

git checkout branche1
echo "bar" >> file2.txt
git commit -a -m "branche1/commit 2"

git checkout master
echo "bar" >> file1.txt
git commit -a -m "master/commit 3"

git merge branche1

git merge branche2

cd ..

# End



