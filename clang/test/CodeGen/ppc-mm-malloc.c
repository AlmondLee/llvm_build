// NOTE: Assertions have been autogenerated by utils/update_cc_test_checks.py
// REQUIRES: native, powerpc-registered-target
// UNSUPPORTED: !powerpc64-
// The stdlib.h included in mm_malloc.h references native system header
// like: bits/libc-header-start.h or features.h, cross-compile it may
// require installing target headers in build env, otherwise expecting
// failures. So this test will focus on native build only.

// RUN: %clang -target powerpc64-unknown-linux-gnu -S -emit-llvm %s -fno-discard-value-names -mllvm -disable-llvm-optzns -o - | llvm-cxxfilt | FileCheck %s

#include <mm_malloc.h>


void __attribute__((noinline))
test_mm_malloc() {
  char *buf = _mm_malloc(100, 16);
  _mm_free(buf);
}

// CHECK-LABEL: @test_mm_malloc

// CHECK: define internal i8* @_mm_malloc(i64 [[REG1:[0-9a-zA-Z_%.]+]], i64 [[REG2:[0-9a-zA-Z_%.]+]])
// CHECK: [[REG3:[0-9a-zA-Z_%.]+]] = alloca i8*, align 8
// CHECK: store i64 [[REG1]], i64* [[REG4:[0-9a-zA-Z_%.]+]], align 8
// CHECK-NEXT: store i64 [[REG2]], i64* [[REG5:[0-9a-zA-Z_%.]+]], align 8
// CHECK-NEXT: store i64 16, i64* [[REG6:[0-9a-zA-Z_%.]+]], align 8
// CHECK-NEXT: [[REG8:[0-9a-zA-Z_%.]+]] = load i64, i64* [[REG5]], align 8
// CHECK-NEXT: [[REG9:[0-9a-zA-Z_%.]+]] = load i64, i64* [[REG6]], align 8
// CHECK-NEXT: [[REG10:[0-9a-zA-Z_%.]+]] = icmp ult i64 [[REG8]], [[REG9]]
// CHECK-NEXT: br i1 [[REG10]], label %[[REG23:[0-9a-zA-Z_%.]+]], label %[[REG24:[0-9a-zA-Z_%.]+]]
// CHECK: [[REG23]]:
// CHECK-NEXT: [[REG25:[0-9a-zA-Z_%.]+]] = load i64, i64* [[REG6]], align 8
// CHECK-NEXT: store i64 [[REG25]], i64* [[REG5]], align 8
// CHECK-NEXT: br label %[[REG24:[0-9a-zA-Z_%.]+]]
// CHECK: [[REG24]]:
// CHECK-NEXT: [[REG26:[0-9a-zA-Z_%.]+]] = load i64, i64* [[REG5]], align 8
// CHECK-NEXT: [[REG27:[0-9a-zA-Z_%.]+]] = load i64, i64* [[REG4]], align 8
// CHECK-NEXT: [[REG28:[0-9a-zA-Z_%.]+]] = call signext i32 @posix_memalign(i8** [[REG29:[0-9a-zA-Z_%.]+]], i64 [[REG26]], i64 [[REG27]])
// CHECK-NEXT: [[REG30:[0-9a-zA-Z_%.]+]] = icmp eq i32 [[REG28]], 0
// CHECK-NEXT: br i1 [[REG30]], label %[[REG31:[0-9a-zA-Z_%.]+]], label %[[REG32:[0-9a-zA-Z_%.]+]]
// CHECK: [[REG31]]:
// CHECK-NEXT: [[REG33:[0-9a-zA-Z_%.]+]] = load i8*, i8** [[REG29]], align 8
// CHECK-NEXT: store i8* [[REG33]], i8** [[REG3]], align 8
// CHECK-NEXT: br label %[[REG19:[0-9a-zA-Z_%.]+]]
// CHECK: [[REG32]]:
// CHECK-NEXT: store i8* null, i8** [[REG3]], align 8
// CHECK-NEXT: br label %[[REG19:[0-9a-zA-Z_%.]+]]
// CHECK: [[REG19]]:
// CHECK-NEXT: [[REG34:[0-9a-zA-Z_%.]+]] = load i8*, i8** [[REG3]], align 8
// CHECK-NEXT: ret i8* [[REG34]]

// CHECK: define internal void @_mm_free(i8* [[REG35:[0-9a-zA-Z_%.]+]])
// CHECK: store i8* [[REG35]], i8** [[REG36:[0-9a-zA-Z_%.]+]], align 8
// CHECK-NEXT: [[REG37:[0-9a-zA-Z_%.]+]] = load i8*, i8** [[REG36]], align 8
// CHECK-NEXT: call void @free(i8* [[REG37]])
// CHECK-NEXT: ret void
