var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('default', ['sass'], function() {
	// place code for your default task here
});

gulp.task('watch', function () {
	gulp.watch('./cat_app/assets/sass/**/*.scss', ['sass']);
});

gulp.task('sass', function () {
	gulp.src('./cat_app/assets/sass/**/*.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('./cat_app/static/css'));
});

gulp.task('sass:watch', function () {
	gulp.watch('./cat_app/assets/sass/**/*.scss', ['sass']);
});