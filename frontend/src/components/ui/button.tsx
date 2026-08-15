import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import type { ButtonHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

const buttonVariants = cva(
  "inline-flex min-h-11 items-center justify-center gap-2 rounded-full px-5 text-sm font-black transition hover:-translate-y-0.5 disabled:pointer-events-none disabled:opacity-55",
  {
    variants: {
      variant: {
        default: "bg-[var(--ink)] text-white hover:bg-neutral-700",
        outline: "border border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--ink)]"
      },
      size: {
        default: "min-h-11 px-5",
        lg: "min-h-12 px-6"
      }
    },
    defaultVariants: {
      variant: "default",
      size: "default"
    }
  }
);

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  };

export function Button({ className, variant, size, asChild, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn(buttonVariants({ variant, size, className }))} {...props} />;
}
