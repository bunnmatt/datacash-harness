var gulp = require('gulp');
var sass = require('gulp-sass');
var minifyCSS = require('gulp-minify-css');


 gulp.task('styles', function() {
  gulp.src('sass/**/*.scss')
  .pipe(sass({
  	errLogToConsole: true
  }))
  .pipe(minifyCSS())
  .pipe(gulp.dest('./static/css/'));
});

 gulp.task('copyfonts', function() {
   gulp.src('./bower_components/font-awesome-sass/assets/fonts/**/*.{ttf,woff*,eof,svg}')
   .pipe(gulp.dest('./static/fonts/'));
});


  gulp.task('default', ['styles', 'copyfonts']);