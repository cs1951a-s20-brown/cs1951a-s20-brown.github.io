#!/bin/bash
for D in */ ;
do
	cd "'$D'"
	target=$(echo "thumbnail.jpg")
	if [ -f $target ]; then
		echo "File $D/$target exists."
	else
		echo "File $D/$target does not exist."
	cd ..
fi
done
