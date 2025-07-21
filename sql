✅ 1. Show All TEXT Blocks (Actual Text Found)

SELECT block.Text
FROM resume_data.textract_output t
CROSS JOIN UNNEST(t.Blocks) AS t(block)
WHERE block.BlockType = 'LINE' AND block.Text IS NOT NULL
LIMIT 20;

✅ 2. Count Total Pages in the Document

SELECT t.DocumentMetadata.Pages AS total_pages
FROM resume_data.textract_output t
LIMIT 1;

✅ 3. Count Total Text Blocks

SELECT COUNT(*) AS total_text_blocks
FROM resume_data.textract_output t
CROSS JOIN UNNEST(t.Blocks) AS t(block)
WHERE block.BlockType = 'LINE';

✅ 4. Search for Email or Contact Information
You can filter for lines likely to be an email or phone:

SELECT block.Text
FROM resume_data.textract_output t
CROSS JOIN UNNEST(t.Blocks) AS t(block)
WHERE block.BlockType = 'LINE'
  AND (block.Text LIKE '%@%' OR block.Text LIKE '%+92%' OR block.Text LIKE '%+1%' OR block.Text LIKE '%03%')
LIMIT 10;


✅ 5. Extract All Words Individually (for word cloud or keyword analysis)

SELECT block.Text
FROM resume_data.textract_output t
CROSS JOIN UNNEST(t.Blocks) AS t(block)
WHERE block.BlockType = 'WORD' AND block.Text IS NOT NULL
LIMIT 30;

✅ 6. Get Confidence of Each Line of Text

SELECT block.Text, block.Confidence
FROM resume_data.textract_output t
CROSS JOIN UNNEST(t.Blocks) AS t(block)
WHERE block.BlockType = 'LINE'
ORDER BY block.Confidence DESC
LIMIT 15;
