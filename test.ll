@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.3 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)
define i32 @main (  ) {
%i = alloca i32
%1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32* %i)
%2= load  i32 , i32* %i
%3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0),  i32 %2)
%index = alloca i32
%4 = alloca i32
store  i32 4 , i32* %4
%5 = load i32 , i32* %4
store i32 %5 , i32* %index
br label %6
;<label>:6:
%7= load  i32 , i32* %index
%8 = alloca i32
store  i32 10 , i32* %8
%9 = load i32 , i32* %8
%10 = icmp slt i32 %9 , %7
br i1 %10 , label %11 , label %16
;<label>:11:
%12= load  i32 , i32* %index
%13 = alloca i32
store  i32 1 , i32* %13
%14 = load i32 , i32* %13
%15 = add i32 %12, %14
store i32 %15 , i32* %index
br label %6
;<label>:16:
%17= load  i32 , i32* %index
%18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0),  i32 %17)
%19 =load i32,  i32* %index
ret i32 %19
}