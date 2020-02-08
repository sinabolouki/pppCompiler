@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [3 x i8] c"%c\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.3 = private unnamed_addr constant [3 x i8] c"%f\00", align 1
@.str.4 = private unnamed_addr constant [7 x i8] c"EQUAL!\00", align 1
@.str.5 = private unnamed_addr constant [13 x i8] c"not equal ! \00", align 1
@.str.6 = private unnamed_addr constant [4 x i8] c"afa\00", align 1

declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)
define i32 @main (  ) {
%i = alloca i32
%1 = alloca i32
store  i32 4 , i32* %1
%2 = load i32 , i32* %1
store i32 %2 , i32* %i
%j = alloca i32
%3= load  i32 , i32* %i
%4 = sub i32 0, %3
store i32 %4 , i32* %j
%c = alloca i32
%5 = alloca i32
store  i32 0 , i32* %5
%6 = load i32 , i32* %5
store i32 %6 , i32* %c
%7 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32* %c)
%8= load  i32 , i32* %c
%9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0),  i32 %8)
%10= load  i32 , i32* %c
%11 = alloca i32
store  i32 0 , i32* %11
%12 = load i32 , i32* %11
%13 = icmp eq i32 %12 , %10
br i1 %13 , label %14 , label %18
;<label>:14:
%15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([7 x i8], [7 x i8]* @.str.4, i32 0, i32 0))
%16 = alloca i32
store  i32 2 , i32* %16
%17 = load i32 , i32* %16
store i32 %17 , i32* %i
br label %20
;<label>: 18:
%19 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([13 x i8], [13 x i8]* @.str.5, i32 0, i32 0))
br label %20
;<label>: 20:
%21 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0), i32* %i)
%22= load  i32 , i32* %j
%23 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0),  i32 %22)
%24 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.6, i32 0, i32 0))
%index = alloca i32
%25 = alloca i32
store  i32 4 , i32* %25
%26 = load i32 , i32* %25
store i32 %26 , i32* %index
br label %27
;<label>:27:
%28= load  i32 , i32* %index
%29 = alloca i32
store  i32 10 , i32* %29
%30 = load i32 , i32* %29
%31 = icmp slt i32 %30 , %28
br i1 %31 , label %32 , label %37
;<label>:32:
%33= load  i32 , i32* %index
%34 = alloca i32
store  i32 1 , i32* %34
%35 = load i32 , i32* %34
%36 = add i32 %33, %35
store i32 %36 , i32* %index
br label %27
;<label>:37:
%38 = alloca i32
store  i32 10 , i32* %38
%39 = load i32 , i32* %38
%40 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i32 0, i32 0),  i32 %39)
%41 =load i32,  i32* %index
ret i32 %41
}
