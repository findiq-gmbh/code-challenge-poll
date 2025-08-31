import z from 'zod';

export const Answer = z.object({
	id: z.number().int().positive().optional(),
	text: z.string().min(1),
	question_id: z.number().int().positive()
});

export type Answer = z.infer<typeof Answer>;
