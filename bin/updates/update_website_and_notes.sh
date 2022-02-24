CurrentNotes=(
  "/home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Spring/CommutativeAlgebra"
  "/home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Spring/CohomologyRepTheory"
  "/home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Spring/FunctionalAnalysis"
  "/home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Spring/SheafCohomology"
  "/home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Spring/ContactTopology"
)

#for val in ${CurrentNotes[@]}; do
   #cd $val; make clean; make all;
#done

pushd ~/website && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com ". ~/.rvm/scripts/rvm && ~/updateWebsite.sh"; 
pushd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes; git stash; git pull;"
pushd ~/dotfiles; git add -A; git commit -am "Save"; git push origin master; popd;

