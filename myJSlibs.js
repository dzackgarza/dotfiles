/* Array Methods */
Array.prototype.flatten = function() {
	return [].concat.apply([], this);
};

Array.prototype.symmetricDifference = function (b) {
	const arrays = [this, b];
	return [].concat(arrays
		.map((arr, i) =>
			arr.filter(elt =>
				!arrays.some((a, j) =>
					i !== j && a.indexOf(elt) >= 0
				)
			)
		)
	).flatten();
};

Array.prototype.product = function(b) {
	return b.map(x =>
		this.map(y => [y, x])
	).flatten();
};

/* Set Methods */
Set.prototype.union = function(b) {
	return new Set( [...this, ...b] );
};

Set.prototype.intersect = function(b) {
	return new Set( [...this].filter(x => b.has(x)) );
};

Set.prototype.difference = function(b) {
	return new Set( [...this].filter(x => !b.has(x)) );
};

Set.prototype.product = function(b) {
	return new Set( [...this].product([...b]) );
};

Set.prototype.cross = Set.prototype.product;

Set.prototype.symmetricDifference = function(b) {
	return new Set( this.difference(b).union(b.difference(this) );
};
