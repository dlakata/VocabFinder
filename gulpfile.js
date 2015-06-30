var gulp = require('gulp');
var less = require('gulp-less');
var watch = require('gulp-watch');
var concat = require('gulp-concat');
var minifyCSS = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var runSequence = require('run-sequence');

gulp.task('less', function() {
    gulp.src('VocabFinder/src/less/**/*.less')
        .pipe(less())
        .pipe(minifyCSS())
        .pipe(concat('style.min.css'))
        .pipe(gulp.dest('VocabFinder/static/css'));
});

gulp.task('js', function() {
    gulp.src(['bower_components/bootstrap/dist/js/bootstrap.js',
        'VocabFinder/src/js/*.js'])
        .pipe(concat('page.js'))
        .pipe(uglify())
        .pipe(gulp.dest('VocabFinder/static/js'));
});

gulp.task('watch', function() {
    gulp.watch('VocabFinder/src/less/**/*.less', ['less']);
    gulp.watch('VocabFinder/src/js/**/*.js', ['js']);
})

gulp.task('default', function(callback) {
  runSequence('less', 'js', 'watch', callback);
})