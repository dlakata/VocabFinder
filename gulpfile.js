var gulp = require('gulp');
var less = require('gulp-less');
var watch = require('gulp-watch');
var concat = require('gulp-concat');
var minifyCSS = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var runSequence = require('run-sequence');

gulp.task('less', function() {
    gulp.src('vocabfinder/src/less/**/*.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(concat('style.min.css'))
        .pipe(gulp.dest('vocabfinder/static/css'));
});

gulp.task('js', function() {
    gulp.src(['bower_components/bootstrap/dist/js/bootstrap.js',
        'bower_components/bootstrap-table/dist/bootstrap-table.js',
        'vocabfinder/src/js/*.js'])
        .pipe(concat('page.js'))
        .pipe(uglify())
        .pipe(gulp.dest('vocabfinder/static/js'));
});

gulp.task('fonts', function() {
    gulp.src('bower_components/bootstrap/fonts/*')
        .pipe(gulp.dest('vocabfinder/static/fonts'))
});

gulp.task('watch', function() {
    gulp.watch('vocabfinder/src/less/*.less', ['less']);
    gulp.watch('vocabfinder/src/js/*.js', ['js']);
});

gulp.task('default', function(callback) {
  runSequence('less', 'js', 'fonts', 'watch', callback);
});
